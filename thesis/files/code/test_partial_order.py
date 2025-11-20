def test_partial_order():
    expiration = (date.today() + timedelta(days=6)).isoformat()

    request_body = {
        "orders": [
            {
                "id": 50,
                "expiration_date": expiration,
                "number": "PARTIAL",
                "pcs_ordered": 8,
                "pcs_printed": 5,
                "printer_work": {
                    "id": 50,
                    "work_name": "PARTIAL_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 3,
                            "time": "01:00:00",
                        }
                    ],
                },
            }
        ],
        "printers": [
            {"id": 1, "name": "Prusa-Mini"},
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
    assert result.summary.total_jobs == 1
    printer_data = result.printers["Prusa-Mini"]
    assert printer_data.job_count == 1
    job = printer_data.jobs[0]
    assert job.plate.pcs == 3
    assert job.order.get_remaining_pcs() == 3
