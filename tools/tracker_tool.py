"""
Tracker Tool

This tool logs each applied job into a local CSV file.
"""

import csv
import os
import time
from typing import Dict, Any


def track_application(job_title: str, company: str, job_url: str, status: str = "applied", portal: str = "LinkedIn") -> Dict[str, Any]:
    """
    Track the application attempt by logging it into a CSV file.

    Args:
        job_title (str): Title of the job
        company (str): Company name
        job_url (str): Link to the job post
        status (str): Status (default: "applied")

    Returns:
        Dict[str, Any]: Summary of what was logged
    """
    try:
        log_path = "data/applied_jobs.csv"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        fieldnames = ["timestamp", "job_title", "company", "job_url", "status", "portal"]

        row = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "job_title": job_title,
            "company": company,
            "job_url": job_url,
            "status": status,
            "portal": portal
        }

        file_exists = os.path.isfile(log_path)

        with open(log_path, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)

        return {
            "result": f"Job tracked successfully: {job_title} at {company}",
            "stats": row,
            "additional_info": {
                "log_file": log_path,
                "status": "logged"
            }
        }

    except Exception as e:
        return {
            "result": "Failed to log application",
            "stats": {},
            "additional_info": {
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }

def log_applied_job(
    job_title: str,
    company: str,
    job_url: str,
    match_score: int,
    portal: str = "LinkedIn"
):
    """
    Wrapper around track_application to include match score in status.
    """
    status = f"applied (match: {match_score}%)"
    return track_application(
        job_title=job_title,
        company=company,
        job_url=job_url,
        status=status,
        portal=portal
    )

