scheduling = APIRouter(dependencies=[Depends(jwt_dependencies.get_verified_payload)])

async def schedule_job(request: ScheduleRequest):
    jobs = OrderConversionService().convert_orders_to_jobs(orders=request.orders)
    status, result = SchedulingService().schedule_with_batches(
        jobs=jobs,
        printers=request.printers,
        alg=ORToolsPrintingScheduler(),
    )
    if status and len(request.printers) > 0 and len(request.orders) > 0:
        response = ScheduleResponse(
            result=result, user_id=request.user_id, orders=request.orders
        ).clean_empty_printers()
        print(response)
        async with httpx.AsyncClient() as client:
            await client.post(
                os.getenv(
                    "WEBHOOK_URL", "http://idrotech-manager.ddev.site/api/webhook" #URL di default ambiente locale di sviluppo
                ),
                json={
                    "message": "Job scheduled successfully",
                    "data": response.model_dump_json(),
                },
                timeout=60,
                headers={"Authorization": f"Bearer {request.callback_token}"},
            )
    else:
        raise Exception(
            "Il modello non ha trovato una soluzione ottimale o accettabile.",
        )


@scheduling.post("/schedule")
async def schedule(request: ScheduleRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(schedule_job, request)
    return {"message": "Scheduling request accepted"}
