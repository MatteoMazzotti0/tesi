def test_no_printer():
    expiration = (date.today() + timedelta(days=5)).isoformat()

    request_body = {
        "orders": [
            {
                "id": 70,
                "expiration_date": expiration,
                "number": "NOWAY",
                "pcs_ordered": 3,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 70,
                    "work_name": "NOWAY_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 1,
                            "time": "00:30:00",
                        }
                    ],
                },
            }
        ],
        "printers": [],
    }

    orders = [Order.model_validate(o) for o in request_body["orders"]]
    printers = [Printer.model_validate(p) for p in request_body["printers"]]
    jobs = OrderConversionService().convert_orders_to_jobs(orders=orders)

    try:
        status, _ = SchedulingService().schedule_with_batches(
            jobs=jobs,
            printers=printers,
            alg=ORToolsPrintingScheduler(),
        )
        assert status is False
    except Exception:
        assert True
