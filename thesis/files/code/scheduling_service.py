class SchedulingService:
    def schedule_with_batches(
        self,
        jobs: List[Job],
        printers: List[Printer],
        alg: OrderingAlg,
    ) -> Tuple[bool, SchedulingResult]:
        batches = self.__split_in_batches(jobs=jobs)

        final_result: SchedulingResult | None = None
        last_schedule_state: SchedulingResult | None = None
        base_datetime = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        suffix_sums_per_batch = self.__get_future_capacity_by_order(batches=batches)

        for i, batch in enumerate(batches): #Divisione in batch
            future_capacity_by_order = suffix_sums_per_batch[i]
            is_last = i == len(batches) - 1
            success, new_schedule = alg.schedule_jobs(
                jobs=batch,
                printers=printers,
                initial_schedule=last_schedule_state,
                base_datetime=base_datetime,
                is_last_schedule=is_last,
                future_capacity_by_order=future_capacity_by_order,
            )
            if not success:
                raise Exception(f"Errore durante la schedulazione del lotto {i + 1}")

            if not final_result:
                final_result = new_schedule
            else:
                final_result = self.__merge_schedules(final_result, new_schedule)
            last_schedule_state = final_result

        if not final_result:
            raise Exception("Result is not a SchedulingResult")

        final_result = self.__set_summary(final_result, base_datetime) #Calcolo del Summary
        return True, final_result
