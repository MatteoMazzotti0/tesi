class SolutionFormatter:
    def __init__(self, context: SchedulerContext):
        self.context = context

    def get_solution_dict(
        self,
        solver: cp_model.CpSolver,
        tasks: Dict[Tuple[str, str], TaskVariable],
        printers: List[Printer],
        status,
    ) -> SchedulingResult:
        result = SchedulingResult(
            status=self.__get_status_string(status),
            success=status in (cp_model.OPTIMAL, cp_model.FEASIBLE),
            printers={},
            summary=Summary(
                total_delay_minutes=0,
                total_jobs=0,
                solver_status=status,
                total_material_changes=0,
                total_makespan_minutes=0,
            ),
        )

        if result.success:
            total_late = 0
            total_jobs = 0
            for pr in printers:
                printer_result = self.__get_printer_schedule(solver, tasks, pr.name)
                result.printers[pr.name] = printer_result
                total_late += printer_result.total_delay_minutes
                total_jobs += len(printer_result.jobs)
            result.summary.total_delay_minutes = total_late
            result.summary.total_jobs = total_jobs
            self.__update_job_start_times(solver, tasks)
        return result


