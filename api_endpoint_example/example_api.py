from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import io

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from report_engine_manager import ReportEngineManager

app = FastAPI(
    title="Sales Report Generator API",
    version="1.0.0",
)


class SalesReportInputModel(BaseModel):
    report_title: str
    sales_data: List[float]
    include_summary: bool = True

    class Config:
        schema_extra = {
            "example": {
                "report_title": "Monthly Sales Report",
                "sales_data": [1000.0, 2000.0, 1500.0],
                "include_summary": True
            }
        }


# Initialize the manager
manager = ReportEngineManager(
    tar_file_dir="images"
)


@app.post(
    "/generate-report",
    summary="Generate a Sales Report",
    description="""
    This endpoint generates a sales report based on the input sales data. 
    The generated report is returned as a downloadable text file.
    """,
    response_description="The generated sales report as a downloadable file.",
    tags=["Reports"]
)
async def generate_report(input_data: SalesReportInputModel):
    """
    Generate a sales report based on the input data provided.
    """
    try:
        # Load the docker image if not already loaded
        manager.load_docker_image("sales-report-engine")
        # Convert the Pydantic model to a dictionary
        input_dict = input_data.dict()
        report_bytes = manager.run_report_engine(
            image_name="sales-report-engine",
            input_data=input_dict
        )
        return StreamingResponse(
            io.BytesIO(report_bytes),
            media_type="application/octet-stream",
            headers={"Content-Disposition": "attachment; filename=report.txt"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
