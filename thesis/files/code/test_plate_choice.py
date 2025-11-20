def test_plate_choice():
    expiration = (date.today() + timedelta(days=6)).isoformat()
    request_body = {
        "orders": [
            {
                "id": 300,
                "expiration_date": expiration,
                "number": "PLATE-CHOICE",
                "pcs_ordered": 10,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 300,
                    "work_name": "PLATE-CHOICE_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 3,
                            "time": "01:00:00",
                        },
                        {
                            "id": 2,
                            "pcs": 5,
                            "time": "01:00:00",
                        },
                    ],
                },
            }
        ],
        "printers": [
            {"id": 1, "name": "Prusa-Plate-Test"},
        ],
    }

    orders = [Order.model_validate(o) for o in request_body["orders"]]
    printers = [Printer.model_validate(p) for p in request_body["printers"]]
    jobs = OrderConversionService().convert_orders_to_jobs(orders=orders)

    status, result = SchedulingService().schedule_with_batches(
        jobs=jobs,
        printers=printers,
        alg=ORToolsPrintingScheduler(),
    )

    assert status is True
    assert result.summary.total_jobs == 2
    assert result.summary.total_delay_minutes == 0

    printer_data = result.printers["Prusa-Plate-Test"]
    assert printer_data.job_count == 2
    for job in printer_data.jobs:
        assert job.plate.pcs == 5
