class ORToolsPrintingScheduler(OrderingAlg):
    def __init__(self):
        self.config = SchedulerConfig()

    def schedule_jobs(
        self,
        jobs: List[Job],
        printers: List[Printer],
        base_datetime: datetime,
        initial_schedule: Optional[SchedulingResult] = None,
        is_last_schedule: bool = False,
        future_capacity_by_order: Optional[Dict[int, int]] = None,
    ) -> Tuple[bool, SchedulingResult]:
        horizon = self.__calculate_horizon(
            jobs=jobs, printers=printers, base_datetime=base_datetime
        )

        context = SchedulerContext.create(
            config=self.config, horizon=horizon, base_datetime=base_datetime
        )

        var_manager = VariableManager(context=context)
        tasks = var_manager.create_variables(jobs=jobs, printers=printers)

        constraint_manager = ConstraintManager(context=context)
        if initial_schedule:
            constraint_manager.add_initial_state_constraints(
                tasks=tasks,
                printers=printers,
                initial_schedule=initial_schedule,
            )
        constraint_manager.add_basic_constraints(
            tasks=tasks, jobs=jobs, printers=printers
        )
        constraint_manager.add_production_constraints(
            tasks=tasks,
            jobs=jobs,
            printers=printers,
            last_schedule_state=initial_schedule,
            future_capacity_by_order=future_capacity_by_order,
        )

        obj_manager = ObjectiveManager(context=context)
        obj_manager.define_objective(
            tasks=tasks,
            jobs=jobs,
            printers=printers,
            final_batch=is_last_schedule,
            last_schedule_state=initial_schedule,
            future_capacity_by_order=future_capacity_by_order,
        )

        if self.config.log_search:
            context.solver.parameters.log_search_progress = True
        context.solver.parameters.max_time_in_seconds = float(
            self.config.solver_timeout
        )

        status = context.solver.Solve(context.model)

        formatter = SolutionFormatter(context=context)
        result = formatter.get_solution_dict(context.solver, tasks, printers, status)
        success = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
        return success, result
