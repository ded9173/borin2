from dataclasses import dataclass, asdict

@dataclass
class SpecificationMaterialDTO:
    spec_mat_id: str
    product_id: str
    material_id: str
    quantity_per_unit: float

    @classmethod
    def from_model(cls, spec) -> "SpecificationMaterialDTO":
        return cls(
            spec_mat_id=str(spec.spec.mat_id), product_id=str(spec.product_id),
            material_id=str(spec.material_id), quantity_per_unit=str(spec.quantity_per_unit),
        )
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class SpecificationOperationDTO:
    spec_op_id: str
    product_id: str
    operation_id: str
    time_norm: float
    op_quantity: float

    @classmethod
    def from_model(cls, spec) -> "SpecificationOperationDTO":
        return cls(
            spec_op_id=str(spec.spec.op_id), product_id=str(spec.product_id),
            operation_id=str(spec.operation.id), time_norm=float(spec.operation.time_norm),
            op_quantity=float(spec.operation.op_quantity),
        )

        def to_dict(self) -> dict:
            return asdict(self)