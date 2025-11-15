class OrderConversionService:
    def convert_orders_to_jobs(self, orders: List[Order]) -> List[Job]:
        result: List[Job] = []
        for order in orders:
            for plate in order.printer_work.plates:
                plate_count = order.get_plate_count(plate=plate)
                for i in range(plate_count):
                    result.append(
                        Job(
                            name=f"Job_{i}_Order_{order.number}",
                            time=plate.time,
                            end_time=datetime.combine(
                                date=(order.expiration_date - timedelta(1)),
                                time=time(23, 59, 59),
                            ),
                            plate=plate,
                            material=order.printer_work.printer_material.name,
                            order=order,
                        )
                    )
        return result
