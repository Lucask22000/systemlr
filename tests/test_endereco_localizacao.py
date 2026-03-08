from models import EnderecoEstoque


def test_build_codigo_localizacao_zero_padding():
    endereco = EnderecoEstoque(
        rua_corredor='A',
        coluna_baia='1',
        nivel_prateleira='2',
        posicao_slot='3'
    )
    assert endereco.build_codigo_localizacao() == 'A-01-02-03'


def test_build_codigo_localizacao_keeps_letters():
    endereco = EnderecoEstoque(
        rua_corredor='RZ',
        coluna_baia='A1',
        nivel_prateleira='B2',
        posicao_slot='C3'
    )
    assert endereco.build_codigo_localizacao() == 'RZ-A1-B2-C3'
