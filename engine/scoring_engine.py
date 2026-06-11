def calculate_score(kp):

    job_houses = {"2","6","10","11"}
    loss_houses = {"5","8","12"}

    job_score = 0
    loss_score = 0

    for p, data in kp.items():
        if p == "risk":
            continue

        houses = set(data["houses"])

        job_score += len(houses.intersection(job_houses))
        loss_score += len(houses.intersection(loss_houses))

    return {
        "job_score": job_score,
        "loss_score": loss_score,
        "result": "JOB STABLE" if job_score > loss_score else "RISK / LOSS"
    }