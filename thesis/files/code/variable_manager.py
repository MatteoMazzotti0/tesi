class VariableManager:
    """Gestisce la creazione delle variabili del modello"""

    def __init__(self, context: SchedulerContext):
        self.context = context

    def create_variables(
        self, jobs: List[Job], printers: List[Printer]
    ) -> Dict[Tuple[str, str], TaskVariable]:
        """Crea tutte le variabili necessarie per il modello"""
        tasks: Dict[Tuple[str, str], TaskVariable] = {}

        for job in jobs:
            for printer in printers:
                task_vars = self.__create_task_variables(job, printer)
                tasks[(job.name, printer.name)] = task_vars

        return tasks

    def __create_task_variables(self, job: Job, printer: Printer) -> TaskVariable:
        """Crea le variabili per un singolo task"""
        job_hash = hash(job.name + printer.name) % 100000

        start = self.context.model.NewIntVar(0, self.context.horizon, f"s_{job_hash}")
        end = self.context.model.NewIntVar(0, self.context.horizon, f"e_{job_hash}")
        assigned = self.context.model.NewBoolVar(f"a_{job_hash}")
        interval = self.context.model.NewOptionalIntervalVar(
            start,
            job.get_time_minutes(),
            end,
            assigned,
            f"i_{job_hash}",
        )

        return TaskVariable(
            start=start,
            end=end,
            assigned=assigned,
            interval=interval,
            material=job.material,
            duration=job.get_time_minutes(),
            deadline=job.get_deadline_minutes(self.context.base_datetime),
            job_instance=job,
        )
