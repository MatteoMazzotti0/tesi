def test_urgent_order():
    urgent_exp = (date.today() - timedelta(days=1)).isoformat()
    normal_exp = (date.today() + timedelta(days=7)).isoformat()

    request_body = {
        "orders": [
            {
                "id": 100,
                "expiration_date": urgent_exp,
                "number": "URGENT",
                "pcs_ordered": 2,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 100,
                    "work_name": "URGENT_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 2,
                            "time": "00:45:00",
                        }
                    ],
                },
            },
            {
                "id": 101,
                "expiration_date": normal_exp,
                "number": "NORMAL",
                "pcs_ordered": 6,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 101,
                    "work_name": "NORMAL_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 3,
                            "time": "01:30:00",
                        }
                    ],
                },
            },
        ],
        "printers": [
            {"id": 1, "name": "OnlyOne"},
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
    assert result.summary.total_jobs == 3
    assert result.summary.total_delay_minutes > 0

    jobs = sorted(
        result.printers["OnlyOne"].jobs, key=lambda j: j.start_time
    )
    assert jobs[0].order.number == "URGENT"
    assert jobs[0].delay_minutes == result.summary.total_delay_minutes
