class ConstraintManager:
    def __init__(self, context: SchedulerContext):
        self.context = context

    def add_initial_state_constraints(
        self,
        tasks: Dict[Tuple[str, str], TaskVariable],
        printers: List[Printer],
        initial_schedule: SchedulingResult,
    ):
        plate_change_time = self.context.config.change_plate_time
        unique_job_names = {key[0] for key in tasks.keys()}
        for printer in printers:
            if (
                printer.name in initial_schedule.printers.keys()
                and initial_schedule.printers[printer.name].jobs
            ):
                printer_schedule = initial_schedule.printers[printer.name]
                last_end_time = max(job.end_time for job in printer_schedule.jobs)
                release_time_minutes = max(
                    0,
                    int(
                        (last_end_time - self.context.base_datetime).total_seconds()
                        // 60
                    ),
                )
                for job_name in unique_job_names:
                    task_key = (job_name, printer.name)
                    if task_key in tasks:
                        task_start_var = tasks[task_key].start
                        self.context.model.Add(
                            task_start_var >= release_time_minutes + plate_change_time
                        ).OnlyEnforceIf(tasks[task_key].assigned)

    def add_basic_constraints(
        self,
        tasks: Dict[Tuple[str, str], TaskVariable],
        jobs: List[Job],
        printers: List[Printer],
    ):
        jobs_map: Dict[str, Job] = {j.name: j for j in jobs}
        self.__add_assignment_constraints(tasks, jobs_map, printers)
        self.__add_no_overlap_constraints(tasks, jobs_map, printers)
        self.__add_start_time_constraints(tasks, jobs_map, printers)

    def add_production_constraints(
        self,
        tasks: Dict[Tuple[str, str], TaskVariable],
        jobs: List[Job],
        printers: List[Printer],
        last_schedule_state: Optional[SchedulingResult],
        future_capacity_by_order: Optional[Dict[int, int]],
    ):
        job_map: Dict[str, Job] = {j.name: j for j in jobs}
        orders: Dict[int, Set[str]] = {}
        for job in jobs:
            oid = job.order.id
            orders.setdefault(oid, set()).add(job.name)
        produced_so_far: Dict[int, int] = {}
        if last_schedule_state:
            for printer_data in last_schedule_state.printers.values():
                for job in printer_data.jobs:
                    oid = job.order.id
                    pcs = job.plate.pcs
                    produced_so_far[oid] = produced_so_far.get(oid, 0) + pcs
        future_cap = future_capacity_by_order or {}
        for oid, job_names in orders.items():
            any_job = next(iter(job_names))
            order = job_map[any_job].order
            already_done = produced_so_far.get(order.id, 0)
            residual = max(0, order.get_remaining_pcs() - already_done)
            cap_future = max(0, int(future_cap.get(order.id, 0)))
            need_now = max(0, residual - cap_future)
            if need_now == 0:
                continue
            produced_terms = []
            for j in job_names:
                pcs = job_map[j].plate.pcs
                for p in printers:
                    produced_terms.append(tasks[(j, p.name)].assigned * int(pcs))
            self.context.model.Add(sum(produced_terms) >= need_now)
