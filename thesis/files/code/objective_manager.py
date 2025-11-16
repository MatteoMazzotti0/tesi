class ObjectiveManager:
    def __init__(self, context: SchedulerContext):
        self.context = context

    def define_objective(
        self,
        tasks: Dict[Tuple[str, str], TaskVariable],
        jobs: List[Job],
        printers: List[Printer],
        final_batch: bool,
        last_schedule_state: Optional[SchedulingResult] = None,
        future_capacity_by_order: Optional[Dict[int, int]] = None,
    ) -> None:
        obj_terms: List = []
        jobs_map: Dict[str, Job] = {j.name: j for j in jobs}
        self.__add_timing_penalties(
            tasks=tasks, jobs_data=jobs_map, printers=printers, obj_terms=obj_terms
        )
        self.__add_makespan_objective(
            tasks=tasks, jobs_data=jobs_map, printers=printers, obj_terms=obj_terms
        )
        self.__add_production_objective(
            tasks=tasks,
            jobs_data=jobs_map,
            printers=printers,
            obj_terms=obj_terms,
            final_batch=final_batch,
            last_schedule_state=last_schedule_state,
            future_capacity_by_order=future_capacity_by_order,
        )
        self.context.model.Minimize(sum(obj_terms))