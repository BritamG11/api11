from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/companies",
    tags=['Companies']
)


# all companies
@router.get("/", response_model=list[schemas.Company])
def get_companies(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    companies = db.query(models.Company).all()
    return companies


# create a company
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Company)
def create_company(post: schemas.CompanyCreate, db: Session = Depends(get_db),
                   user_id: int = Depends(oauth2.get_current_user)):
    new_company = models.Company(**post.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


# Fetching individual company
@router.get("/{id}", response_model=schemas.Company)
def get_company(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    company = db.query(models.Company).filter(models.Company.id == id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"company with id: {id} was not found")
    return {"company_detail": company}


# Delete company
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    delete_company = db.query(models.Company).filter(models.Company.id == id)
    if delete_company.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"company with id:{id} does not exist")
    delete_company.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update company
@router.put("/{id}", response_model=schemas.Company)
def update_company(id: int, updated_company: schemas.CompanyCreate, db: Session = Depends(get_db),
                   user_id: int = Depends(oauth2.get_current_user)):
    company_query = db.query(models.Company).filter(models.Company.id == id)
    company = company_query.first()

    if company == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"company with id: {id} does not exist")
    company_query.update(updated_company.dict(), synchronize_session=False)
    db.commit()

    return company_query.first()
