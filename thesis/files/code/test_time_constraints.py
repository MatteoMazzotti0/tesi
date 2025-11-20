def test_time_constraints():
    expiration = (date.today() + timedelta(days=30)).isoformat()
    request_body = {
        "orders": [
            {
                "id": 200,
                "expiration_date": expiration,
                "number": "TEST-VINCOLI-ORARI-WEEKEND",
                "pcs_ordered": 22,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 200,
                    "work_name": "TEST-VINCOLI-ORARI-WEEKEND_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 1,
                            "time": "03:00:00",
                        }
                    ],
                },
            }
        ],
        "printers": [
            {"id": 1, "name": "Stampante-Test"},
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
    assert result.summary.total_jobs == 22
    assert result.summary.total_delay_minutes == 0

    for job in result.printers["Stampante-Test"].jobs:
        start: datetime = job.start_time
        assert start.weekday() < 5
        assert 9 <= start.hour < 18
