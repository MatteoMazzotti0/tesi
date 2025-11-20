def test_single_order():
    expiration = (date.today() + timedelta(days=7)).isoformat()

    request_body = {
        "orders": [
            {
                "id": 1,
                "expiration_date": expiration,
                "number": "ORD-001",
                "pcs_ordered": 6,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 1,
                    "work_name": "ORD-001_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 3,
                            "time": "02:00:00",
                        }
                    ],
                },
            }
        ],
        "printers": [
            {"id": 1, "name": "PRUSA-01"},
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
    assert result.printers["PRUSA-01"].job_count == 2
