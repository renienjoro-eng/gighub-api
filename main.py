from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="GigHub API - C027-01-0882/2024",
    description="An API to manage gig listings for GigHub freelancing platform",
    version="1.0.0"
)

#The in-memory database
gigs_db = [
    {
        "id": 1,
        "title": "Build an E-commerce Website",
        "description": "Develop a fully responsive e-commerce website with user authentication, product management, and secure payment integration.",
        "category": "Development",
        "budget": 85000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Grace Wanjiku"
    },
    {
        "id": 2,
        "title": "Design a Restaurant Logo",
        "description": "Create a modern and memorable logo for a new restaurant that reflects its brand identity and attracts customers.",
        "category": "Design",
        "budget": 12000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Brian Otieno"
    },
   
    {
        "id": 3,
        "title": "Develop a Mobile Banking App",
        "description": "Build a secure Android mobile banking application with account management, transfers, and transaction history features.",
        "category": "Development",
        "budget": 150000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Kevin Mwangi"
    },
    {
        "id": 4,
        "title": "Design Social Media Banners",
        "description": "Create attractive promotional banners for Facebook, Instagram, and LinkedIn marketing campaigns using modern design principles.",
        "category": "Design",
        "budget": 10000,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Faith Njeri"
    },
    {
        "id": 5,
        "title": "Write Product Descriptions",
        "description": "Prepare compelling and persuasive product descriptions for an online electronics store to improve customer engagement.",
        "category": "Writing",
        "budget": 14000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Samuel Kiptoo"
    },
    {
        "id": 6,
        "title": "Create an Inventory System",
        "description": "Develop a desktop inventory management system with stock tracking, reporting, and user authentication capabilities.",
        "category": "Development",
        "budget": 95000,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Esther Chebet"
    },
    {
        "id": 7,
        "title": "Design Event Posters",
        "description": "Design creative posters for a technology conference that effectively communicate event details and branding.",
        "category": "Design",
        "budget": 9000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Daniel Kimani"
    },
   
   
]

# Pydantic Models
class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., pattern="^(Development|Design|Writing)$")
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=3, max_length=100)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(
        None,
        pattern="^(Open|In Progress|Closed)$"
    )


# GET all gigs
@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):

    results = gigs_db

    if category:
        results = [
            gig for gig in results
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] <= max_budget
        ]

    return results

# SEARCH gigs by title
@app.get("/gigs/search")
def search_gigs(q: str):

    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results

# GET gig by ID
@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):

    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")



# CREATE new gig
@app.post("/gigs")
def create_gig(gig: GigCreate):

    new_id = max(item["id"] for item in gigs_db) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }


# UPDATE gig
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, updates: GigUpdate):

    for gig in gigs_db:

        if gig["id"] == gig_id:

            if updates.budget is not None:
                gig["budget"] = updates.budget

            if updates.status is not None:
                gig["status"] = updates.status

            return {
                "message": "Gig updated successfully",
                "gig": gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")


# DELETE gig
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):

    for gig in gigs_db:

        if gig["id"] == gig_id:
            gigs_db.remove(gig)

            return {
                "message": "Gig deleted successfully"
            }

    raise HTTPException(status_code=404, detail="Gig not found")
