def test_materials_optimization():
    exp_pla = (date.today() + timedelta(days=4)).isoformat()
    exp_petg = (date.today() + timedelta(days=5)).isoformat()

    request_body = {
        "orders": [
            {
                "id": 10,
                "expiration_date": exp_pla,
                "number": "ORD-PLA",
                "pcs_ordered": 9,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 10,
                    "work_name": "ORD-PLA_WORK",
                    "printer_material": {"id": 1, "name": "PLA"},
                    "plates": [
                        {
                            "id": 1,
                            "pcs": 3,
                            "time": "01:00:00",
                        }
                    ],
                },
            },
            {
                "id": 11,
                "expiration_date": exp_petg,
                "number": "ORD-PETG",
                "pcs_ordered": 6,
                "pcs_printed": 0,
                "printer_work": {
                    "id": 11,
                    "work_name": "ORD-PETG_WORK",
                    "printer_material": {"id": 2, "name": "PETG"},
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
            {"id": 1, "name": "MK3S"},
            {"id": 2, "name": "BambuLab"},
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
    assert result.summary.total_jobs == 5
    assert result.summary.total_delay_minutes == 0

    for printer_data in result.printers.values():
        if printer_data.job_count == 0:
            continue
        materials = {job.material for job in printer_data.jobs}
        assert len(materials) == 1
