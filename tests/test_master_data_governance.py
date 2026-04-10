import pytest

from app import db
from app.exceptions import ValidationError
from app.services.master_data import (
    normalize_cost_center,
    validate_cancel_reason_classified,
    validate_employee_payload,
    validate_movement_reason_classified,
    validate_payment_options_configuration,
    validate_stock_master_payload,
    validate_supplier_payload,
)
from models import EmpresaConfig, Estoque, Fornecedor, Funcionario


def test_validate_supplier_payload_blocks_incomplete_active_supplier():
    with pytest.raises(ValidationError):
        validate_supplier_payload(
            nome='Fornecedor Incompleto',
            documento='',
            telefone='',
            email='',
            endereco_cidade='',
            tipo_produtos_fornece='',
            ativo=True,
        )


def test_validate_employee_payload_blocks_active_employee_without_department():
    with pytest.raises(ValidationError):
        validate_employee_payload(
            nome='Funcionario Teste',
            email='funcionario@test.local',
            role='operador',
            cargo='Repositor',
            departamento='',
            ativo=True,
        )


def test_validate_stock_master_payload_blocks_active_stock_without_branch_code():
    with pytest.raises(ValidationError):
        validate_stock_master_payload(nome='Loja Centro', codigo_filial='', ativo=True)


def test_normalize_cost_center_blocks_unknown_cost_center():
    with pytest.raises(ValidationError):
        normalize_cost_center('marketing')


def test_validate_movement_reason_classified_blocks_unknown_reason():
    with pytest.raises(ValidationError):
        validate_movement_reason_classified('qualquer_coisa', tipo='saida')


def test_validate_cancel_reason_classified_requires_clear_or_standard_reason():
    with pytest.raises(ValidationError):
        validate_cancel_reason_classified('erro', entity_label='pedido')


def test_validate_payment_options_configuration_blocks_missing_label():
    with pytest.raises(ValidationError):
        validate_payment_options_configuration('pix', channel='pdv')


def test_novo_fornecedor_blocks_incomplete_active_supplier(authenticated_client, csrf_token):
    response = authenticated_client.post('/fornecedores/novo', data={
        'nome': 'Fornecedor Sem Cidade',
        'telefone': '65999999999',
        'ativo': 'on',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 200
    assert Fornecedor.query.filter_by(nome='Fornecedor Sem Cidade').first() is None


def test_novo_estoque_blocks_active_stock_without_branch_code(authenticated_client, csrf_token):
    response = authenticated_client.post('/estoques/novo', data={
        'nome': 'Filial Sem Codigo',
        'ativo': 'on',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 200
    assert Estoque.query.filter_by(nome='Filial Sem Codigo').first() is None


def test_criar_funcionario_blocks_missing_department(authenticated_client, csrf_token):
    response = authenticated_client.post('/funcionarios/novo', data={
        'nome': 'Funcionario Sem Departamento',
        'email': 'semdepartamento@test.local',
        'senha': '123456',
        'confirmacao_senha': '123456',
        'role': 'operador',
        'cargo': 'Repositor',
        'departamento': '',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    assert Funcionario.query.filter_by(email='semdepartamento@test.local').first() is None


def test_editar_empresa_blocks_malformed_payment_configuration(authenticated_client, csrf_token):
    empresa = EmpresaConfig(nome_fantasia='Empresa Teste')
    db.session.add(empresa)
    db.session.commit()

    response = authenticated_client.post('/empresa', data={
        'pagamentos_pdv_config': 'pix',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 200
    db.session.refresh(empresa)
    assert empresa.pagamentos_pdv_json is None


def test_financeiro_lancamento_blocks_unknown_cost_center(authenticated_client, csrf_token):
    response = authenticated_client.post('/financeiro/lancamentos', data={
        'tipo': 'despesa',
        'descricao': 'Despesa sem centro padronizado',
        'valor': '10,00',
        'referencia_documento': 'DOC-1',
        'centro_custo': 'marketing',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
