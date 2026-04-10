import unittest

from utils.endereco_codigo import (
    configurar_endereco,
    gerar_codigo_localizacao_supermercado,
    montar_endereco,
    parse_endereco,
    validar_endereco_supermercado_payload,
    validar_endereco,
)


class EnderecoCodigoTestCase(unittest.TestCase):
    def setUp(self):
        configurar_endereco(zonas_permitidas={'ZP', 'ZR', 'ZQ', 'ZD'}, permitir_nivel_zero=True)

    def test_montar_endereco_valido(self):
        codigo = montar_endereco(cd=1, zona='P', rua=5, rack=3, nivel=2, vao=12, lado='A')
        self.assertEqual(codigo, 'CD01-ZP-R05-RK03-N02-V12-LA')

    def test_montar_endereco_lado_direita_e_zona_com_prefixo(self):
        codigo = montar_endereco(cd=12, zona='ZR', rua=9, rack=1, nivel=0, vao=7, lado='DIR')
        self.assertEqual(codigo, 'CD12-ZR-R09-RK01-N00-V07-LB')

    def test_parse_endereco_normaliza_minusculo_espaco_e_underscore(self):
        partes = parse_endereco('cd01_zp r05_rk03_n02_v12_la')
        esperado = {
            'cd': 1,
            'zona': 'ZP',
            'rua': 5,
            'rack': 3,
            'nivel': 2,
            'vao': 12,
            'lado': 'LA',
        }
        self.assertEqual(partes, esperado)

    def test_validar_endereco_invalido_por_campo(self):
        resp = validar_endereco('CD00-ZP-R00-RK03-N02-V12-LA')
        self.assertFalse(resp['valido'])
        self.assertTrue(resp['erros'])
        self.assertEqual(resp['partes'], {})

    def test_validar_endereco_invalido_zona_nao_permitida(self):
        resp = validar_endereco('CD01-ZX-R05-RK03-N02-V12-LA')
        self.assertFalse(resp['valido'])
        self.assertIn('nao permitida', resp['erros'][0])

    def test_montar_endereco_rejeita_zona_nao_alfanumerica(self):
        with self.assertRaises(ValueError):
            montar_endereco(cd=1, zona='P@', rua=5, rack=3, nivel=2, vao=12, lado='A')

    def test_montar_endereco_rejeita_lado_nao_alfanumerico(self):
        with self.assertRaises(ValueError):
            montar_endereco(cd=1, zona='P', rua=5, rack=3, nivel=2, vao=12, lado='A-1')

    def test_configuracao_nivel_zero_desabilitado(self):
        configurar_endereco(permitir_nivel_zero=False)
        resp = validar_endereco('CD01-ZP-R05-RK03-N00-V12-LA')
        self.assertFalse(resp['valido'])
        self.assertIn('nivel', resp['erros'][0].lower())

    def test_configuracao_zonas_personalizadas(self):
        configurar_endereco(zonas_permitidas={'ZA1', 'ZB2'})
        codigo = montar_endereco(cd=2, zona='A1', rua=1, rack=1, nivel=1, vao=1, lado='ESQ')
        self.assertEqual(codigo, 'CD02-ZA1-R01-RK01-N01-V01-LA')

        invalido = validar_endereco('CD02-ZP-R01-RK01-N01-V01-LA')
        self.assertFalse(invalido['valido'])


class EnderecoSupermercadoCodigoTestCase(unittest.TestCase):
    def test_gerar_codigo_rack(self):
        codigo = gerar_codigo_localizacao_supermercado(
            loja_cd='lj01',
            setor_zona='bebidas',
            tipo_estrutura='rack',
            rua_corredor='3',
            rack_estante='2',
            nivel_prateleira='1',
            posicao_slot='8',
            lado='a',
        )
        self.assertEqual(codigo, 'LJ01-BEB-R03-RK02-N01-V08-LA')

    def test_gerar_codigo_area_aberta(self):
        codigo = gerar_codigo_localizacao_supermercado(
            loja_cd='LJ01',
            setor_zona='frente_loja',
            tipo_estrutura='area_aberta',
            ponto_local='Gondola 12 - Prateleira 3',
        )
        self.assertEqual(codigo, 'LJ01-FL-G12-P03')

    def test_validacao_condicional_rack(self):
        payload = {
            'loja_cd': 'LJ01',
            'setor_zona': 'bebidas',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'rack',
            'rua_corredor': '3',
            'rack_estante': '2',
            'nivel_prateleira': '1',
            'posicao_slot': '8',
            'lado': 'B',
            'controle_validade': 'fifo',
        }
        dados = validar_endereco_supermercado_payload(payload)
        self.assertEqual(dados['codigo_localizacao'], 'LJ01-BEB-R03-RK02-N01-V08-LB')
        self.assertIsNone(dados['ponto_local'])

    def test_validacao_condicional_area_aberta(self):
        payload = {
            'loja_cd': 'LJ01',
            'setor_zona': 'frente_loja',
            'tipo_area': 'frente_loja',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Camara fria 1',
            'controle_validade': 'nenhum',
        }
        dados = validar_endereco_supermercado_payload(payload)
        self.assertTrue(dados['codigo_localizacao'].startswith('LJ01-FL-'))
        self.assertIsNone(dados['rua_corredor'])

    def test_validacao_rack_sem_campos_obrigatorios(self):
        payload = {
            'loja_cd': 'LJ01',
            'setor_zona': 'bebidas',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'rack',
            'controle_validade': 'fifo',
        }
        with self.assertRaises(ValueError):
            validar_endereco_supermercado_payload(payload)


if __name__ == '__main__':
    unittest.main()
