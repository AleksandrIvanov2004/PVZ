from fastapi import APIRouter, HTTPException, Depends
from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.schemas.user import UserSchema
from project.infrastructure.postgres.repository.car_repo import CarRepository
from project.schemas.car import CarSchema
from project.infrastructure.postgres.repository.driver_repo import DriverRepository
from project.schemas.driver import DriverSchema
from project.infrastructure.postgres.repository.pick_up_point_repo import PickUpPointRepository
from project.schemas.pick_up_point import PickUpPointSchema
from project.infrastructure.postgres.repository.worker_repo import WorkerRepository
from project.schemas.worker import WorkerSchema
from project.infrastructure.postgres.repository.working_shift_repo import WorkingShiftRepository
from project.schemas.working_shift import WorkingShiftSchema
from project.infrastructure.postgres.repository.supply_repo import SupplyRepository
from project.schemas.supply import SupplySchema
from project.infrastructure.postgres.repository.product_repo import ProductRepository
from project.schemas.product import ProductSchema
from project.schemas.login import  LoginSchema
from project.infrastructure.security.auth import get_current_user, allow_only_admin

router = APIRouter()
@router.get("/all_users", response_model=list[UserSchema])
async def get_all_users(current_user: dict = Depends(allow_only_admin)) -> list[UserSchema]:
    user_repo = UserRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_users = await user_repo.get_all_users(session=session)
    return all_users

@router.get("/users/{id}", response_model=UserSchema)
async def get_user_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        user = await user_repo.get_user_by_id(session=session, id_user=id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/users", response_model=UserSchema)
async def insert_user(user: UserSchema, current_user: dict = Depends(allow_only_admin)) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        new_user = await user_repo.insert_user(session=session, login=user.login, passw=user.password,
                                               surname=user.surname, name=user.name, last_name=user.last_name,
                                               age=user.age, phone_number=user.phone_number, region=user.region,
                                               role=user.role)

    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to insert user")

    return new_user


@router.delete("/users/{id}", response_model=dict)
async def delete_user_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        deleted = await user_repo.delete_user_by_id(session=session, id_user=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found or failed to delete")

    return {"message": "User deleted successfully"}


@router.put("/users/{id}", response_model=UserSchema)
async def update_user_by_id(id: int, user: UserSchema, current_user: dict = Depends(allow_only_admin)) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        updated_user = await user_repo.update_user_by_id(session=session, id_user=id, login=user.login, password=user.password,
                                                         surname=user.surname, name=user.name, last_name=user.last_name,
                                                         age=user.age, phone_number=user.phone_number, region=user.region,
                                                         role=user.role)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or failed to update")

    return updated_user


@router.post("/login")
async def login(user: LoginSchema) -> dict:
    users_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_repo.check_connection(session=session)
        auth_response = await users_repo.login_user(session=session, login=user.login, passw=user.password)

    return auth_response


@router.get("/all_cars", response_model=list[CarSchema])
async def get_all_cars() -> list[CarSchema]:
    car_repo = CarRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await car_repo.check_connection(session=session)
        all_cars = await car_repo.get_all_cars(session=session)
    return all_cars

@router.get("/cars/{id}", response_model=CarSchema)
async def get_car_by_id(id: int) -> CarSchema:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        car = await car_repo.get_car_by_id(session=session, id_car=id)

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return car


@router.post("/cars", response_model=CarSchema)
async def insert_car(car: CarSchema, current_user: dict = Depends(allow_only_admin)) -> CarSchema:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        new_car = await car_repo.insert_car(session=session, id=car.id)

    if not new_car:
        raise HTTPException(status_code=500, detail="Failed to insert car")

    return new_car


@router.delete("/cars/{id}", response_model=dict)
async def delete_car_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        deleted = await car_repo.delete_car_by_id(session=session, id_car=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found or failed to delete")

    return {"message": "Car deleted successfully"}

@router.put("/cars/{id}", response_model=CarSchema)
async def update_car_by_id(id: int, car: CarSchema) -> CarSchema:
    car_repo = CarRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await car_repo.check_connection(session=session)
        updated_car = await car_repo.update_car_by_id(session=session, id_car=id, number=car.number, region=car.region)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found or failed to update")

    return updated_car



@router.get("/all_drivers", response_model=list[DriverSchema])
async def get_all_drivers() -> list[DriverSchema]:
    driver_repo = DriverRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await driver_repo.check_connection(session=session)
        all_drivers = await driver_repo.get_all_drivers(session=session)
    return all_drivers

@router.get("/drivers/{id}", response_model=DriverSchema)
async def get_driver_by_id(id: int) -> DriverSchema:
    driver_repo = DriverRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await driver_repo.check_connection(session=session)
        driver = await driver_repo.get_driver_by_id(session=session, id_driver=id)

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver


@router.post("/drivers", response_model=DriverSchema)
async def insert_driver(driver: DriverSchema, current_user: dict = Depends(allow_only_admin)) -> DriverSchema:
    driver_repo = DriverRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await driver_repo.check_connection(session=session)
        new_driver = await driver_repo.insert_driver(session=session, car_id=driver.car_id
                                                     , user_id=driver.user_id)

    if not new_driver:
        raise HTTPException(status_code=500, detail="Failed to insert driver")

    return new_driver


@router.delete("/drivers/{id}", response_model=dict)
async def delete_driver_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    driver_repo = DriverRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await driver_repo.check_connection(session=session)
        deleted = await driver_repo.delete_driver_by_id(session=session, id_driver=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Driver not found or failed to delete")

    return {"message": "Driver deleted successfully"}


@router.put("/drivers/{id}", response_model=DriverSchema)
async def update_driver_by_id(id: int, driver: DriverSchema) -> DriverSchema:
    driver_repo = DriverRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await driver_repo.check_connection(session=session)
        updated_driver = await driver_repo.update_driver_by_id(session=session, id_driver=id
                                                               , car_id=driver.car_id
                                                               , user_id=driver.user_id)
    if not updated_driver:
        raise HTTPException(status_code=404, detail="Driver not found or failed to update")

    return updated_driver



@router.get("/all_pick_up_points", response_model=list[PickUpPointSchema])
async def get_all_pick_up_points() -> list[PickUpPointSchema]:
    pick_up_point_repo = PickUpPointRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await pick_up_point_repo.check_connection(session=session)
        all_pick_up_points = await pick_up_point_repo.get_all_pick_up_points(session=session)
    return all_pick_up_points

@router.get("/pick_up_points/{id}", response_model=PickUpPointSchema)
async def get_pick_up_point_by_id(id: int) -> PickUpPointSchema:
    pick_up_point_repo = PickUpPointRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await pick_up_point_repo.check_connection(session=session)
        pick_up_point = await pick_up_point_repo.get_pick_up_point_by_id(session=session, id_pick_up_point=id)

    if not pick_up_point:
        raise HTTPException(status_code=404, detail="Pick up point not found")

    return pick_up_point


@router.post("/pick_up_points", response_model=PickUpPointSchema)
async def insert_pick_up_point(pick_up_point: PickUpPointSchema, current_user: dict = Depends(allow_only_admin)) -> PickUpPointSchema:
    pick_up_point_repo = PickUpPointRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await pick_up_point_repo.check_connection(session=session)
        new_pick_up_point = await pick_up_point_repo.insert_pick_up_point(session=session, region=pick_up_point.region,
                                                                          address=pick_up_point.address)

    if not new_pick_up_point:
        raise HTTPException(status_code=500, detail="Failed to insert pick up point")

    return PickUpPointSchema


@router.delete("/pick_up_points/{id}", response_model=dict)
async def delete_pick_up_point_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    pick_up_point_repo = PickUpPointRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await pick_up_point_repo.check_connection(session=session)
        deleted = await pick_up_point_repo.delete_pick_up_point_by_id(session=session, id_pick_up_point=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Pick up point not found or failed to delete")

    return {"message": "Pick up point deleted successfully"}


@router.put("/pick_up_points/{id}", response_model=PickUpPointSchema)
async def update_pick_up_point_by_id(id: int, pick_up_point: PickUpPointSchema) -> PickUpPointSchema:
    pick_up_point_repo = PickUpPointRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await pick_up_point_repo.check_connection(session=session)
        updated_pick_up_point = await pick_up_point_repo.update_pick_up_point_by_id(session=session, id_pick_up_point=id,
                                                                                    region=pick_up_point.region,
                                                                                    address=pick_up_point.address)
    if not updated_pick_up_point:
        raise HTTPException(status_code=404, detail="Pick up point not found or failed to update")

    return updated_pick_up_point



@router.get("/all_workers", response_model=list[WorkerSchema])
async def get_all_workers() -> list[WorkerSchema]:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        all_workers = await worker_repo.get_all_workers(session=session)
    return all_workers

@router.get("/workers/{id}", response_model=WorkerSchema)
async def get_worker_by_id(id: int) -> WorkerSchema:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        worker = await worker_repo.get_worker_by_id(session=session, id_worker=id)

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    return worker


@router.post("/workers", response_model=WorkerSchema)
async def insert_worker(worker: WorkerSchema, current_user: dict = Depends(allow_only_admin)) -> WorkerSchema:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        new_worker = await worker_repo.insert_worker(session=session, user_id=worker.user_id,
                                                     pick_up_point_id=worker.pick_up_point_id)

    if not new_worker:
        raise HTTPException(status_code=500, detail="Failed to insert worker")

    return new_worker


@router.delete("/workers/{id}", response_model=dict)
async def delete_worker_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        deleted = await worker_repo.delete_worker_by_id(session=session, id_worker=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Worker not found or failed to delete")

    return {"message": "Worker deleted successfully"}


@router.put("/workers/{id}", response_model=WorkerSchema)
async def update_worker_by_id(id: int, worker: WorkerSchema) -> WorkerSchema:
    worker_repo = WorkerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await worker_repo.check_connection(session=session)
        updated_worker = await worker_repo.update_worker_by_id(session=session, id_worker=id, user_id=worker.user_id,
                                                               pick_up_point_id=worker.pick_up_point_id)
    if not updated_worker:
        raise HTTPException(status_code=404, detail="Worker not found or failed to update")

    return updated_worker



@router.get("/all_working_shifts", response_model=list[WorkingShiftSchema])
async def get_all_working_shifts() -> list[WorkingShiftSchema]:
    working_shift_repo = WorkingShiftRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await working_shift_repo.check_connection(session=session)
        all_working_shifts = await working_shift_repo.get_all_working_shifts(session=session)
    return all_working_shifts

@router.get("/working_shifts/{id}", response_model=WorkingShiftSchema)
async def get_working_shift_by_id(id: int) -> WorkingShiftSchema:
    working_shift_repo = WorkingShiftRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await working_shift_repo.check_connection(session=session)
        working_shift = await working_shift_repo.get_working_shift_by_id(session=session, id_working_shift=id)

    if not working_shift:
        raise HTTPException(status_code=404, detail="Working shift not found")

    return working_shift


@router.post("/working_shifts", response_model=WorkingShiftSchema)
async def insert_working_shift(working_shift: WorkingShiftSchema, current_user: dict = Depends(allow_only_admin)) -> WorkingShiftSchema:
    working_shift_repo = WorkingShiftRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await working_shift_repo.check_connection(session=session)
        new_working_shift = await working_shift_repo.insert_working_shift(session=session, user_id=working_shift.user_id,
                                                                          start_time=working_shift.start_time,
                                                                          end_time=working_shift.end_time)

    if not new_working_shift:
        raise HTTPException(status_code=500, detail="Failed to insert working shift")

    return new_working_shift

@router.delete("/working_shifts/{id}", response_model=dict)
async def delete_working_shift_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    working_shift_repo = WorkingShiftRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await working_shift_repo.check_connection(session=session)
        deleted = await working_shift_repo.delete_working_shift_by_id(session=session, id_working_shift=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Working shift not found or failed to delete")

    return {"message": "Working shift deleted successfully"}


@router.put("/working_shifts/{id}", response_model=WorkingShiftSchema)
async def update_working_shift_by_id(id: int, working_shift: WorkingShiftSchema) -> WorkingShiftSchema:
    working_shift_repo = WorkingShiftRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await working_shift_repo.check_connection(session=session)
        updated_working_shift = await working_shift_repo.update_working_shift_by_id(session=session, id_working_shift=id,
                                                                                    user_id=working_shift.user_id,
                                                                                    start_time=working_shift.start_time,
                                                                                    end_time=working_shift.end_time
                                                                                    )
    if not updated_working_shift:
        raise HTTPException(status_code=404, detail="Working shift not found or failed to update")

    return updated_working_shift



@router.get("/all_supplies", response_model=list[SupplySchema])
async def get_all_supplies() -> list[SupplySchema]:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await supply_repo.check_connection(session=session)
        all_supplies = await supply_repo.get_all_supplies(session=session)
    return all_supplies

@router.get("/supplies/{id}", response_model=SupplySchema)
async def get_supply_by_id(id: int) -> SupplySchema:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supply_repo.check_connection(session=session)
        supply = await supply_repo.get_supply_by_id(session=session, id_supply=id)

    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")

    return supply


@router.post("/supplies", response_model=SupplySchema)
async def insert_supply(supply: SupplySchema, current_user: dict = Depends(allow_only_admin)) -> SupplySchema:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supply_repo.check_connection(session=session)
        new_supply = await supply_repo.insert_supply(session=session, driver_id=supply.driver_id,
                                                     pick_up_point_id=supply.pick_up_point_id,
                                                     time=supply.time)

    if not new_supply:
        raise HTTPException(status_code=500, detail="Failed to insert supply")

    return new_supply


@router.delete("/supplies/{id}", response_model=dict)
async def delete_supply_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supply_repo.check_connection(session=session)
        deleted = await supply_repo.delete_supply_by_id(session=session, id_supply=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Supply not found or failed to delete")

    return {"message": "Supply deleted successfully"}


@router.put("/supplies/{id}", response_model=SupplySchema)
async def update_supply_by_id(id: int, supply: SupplySchema) -> SupplySchema:
    supply_repo = SupplyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supply_repo.check_connection(session=session)
        updated_supply = await supply_repo.update_supply_by_id(session=session, id_supply=id, driver_id=supply.driver_id,
                                                               pick_up_point_id=supply.pick_up_point_id,
                                                               time=supply.time)
    if not updated_supply:
        raise HTTPException(status_code=404, detail="Supply not found or failed to update")

    return updated_supply



@router.get("/all_products", response_model=list[ProductSchema])
async def get_all_products() -> list[ProductSchema]:
    product_repo = ProductRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await product_repo.check_connection(session=session)
        all_products = await product_repo.get_all_products(session=session)
    return all_products

@router.get("/products/{id}", response_model=ProductSchema)
async def get_product_by_id(id: int) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        product = await product_repo.get_product_by_id(session=session, id_product=id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/products", response_model=ProductSchema)
async def insert_product(product: ProductSchema, current_user: dict = Depends(allow_only_admin)) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        new_product = await product_repo.insert_product(session=session, supply_id=product.supply_id
                                                        , status=product.status)

    if not new_product:
        raise HTTPException(status_code=500, detail="Failed to insert product")

    return new_product


@router.delete("/products/{id}", response_model=dict)
async def delete_product_by_id(id: int, current_user: dict = Depends(allow_only_admin)) -> dict:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        deleted = await product_repo.delete_product_by_id(session=session, id_product=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found or failed to delete")

    return {"message": "Product deleted successfully"}


@router.put("/products/{id}", response_model=ProductSchema)
async def update_product_by_id(id: int, product: ProductSchema) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        updated_product = await product_repo.update_product_by_id(session=session, id_product=id, supply_id=product.supply_id
                                                                 , status=product.status)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or failed to update")

    return updated_product


