"""
Motor de Regras de Negócio - Base de Conhecimento do WineBrain
Implementa as regras de decisão prescritiva
"""

from typing import Dict, List, Any
from enum import Enum


class AcaoRecomendada(str, Enum):
    """Tipos de ações recomendadas"""
    VINHOS_PREMIUM = "recomendar_vinhos_premium"
    EVENTOS_EXCLUSIVOS = "convidar_eventos_exclusivos"
    CUPOM_REATIVACAO = "enviar_cupom_reativacao"
    PESQUISA_SATISFACAO = "enviar_pesquisa_satisfacao"
    UPGRADE_CLUBE = "oferecer_upgrade_clube"
    ADESAO_CLUBE = "recomendar_adesao_clube"
    PROGRAMA_FIDELIDADE = "incluir_programa_fidelidade"
    CAMPANHA_REENGAJAMENTO = "ativar_campanha_reengajamento"
    DEGUSTACAO = "convidar_degustacao"
    NENHUMA = "nenhuma_acao"


class NivelPrioridade(str, Enum):
    """Níveis de prioridade das ações"""
    CRITICA = "critica"
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"


class RuleEngine:
    """Motor de Regras de Negócio"""
    
    def __init__(self):
        # Limiares configuráveis
        self.ENGAJAMENTO_ALTO = 8
        self.ENGAJAMENTO_MEDIO_MIN = 4
        self.ENGAJAMENTO_MEDIO_MAX = 7
        self.ENGAJAMENTO_BAIXO = 4
        self.DESCONTO_REATIVACAO = 0.20
        self.MIN_COMPRAS_FIDELIDADE = 3
    
    def avaliar_cliente(self, cliente_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Avalia um cliente e retorna recomendações baseadas nas regras de negócio
        
        Args:
            cliente_data: Dicionário com dados do cliente
            
        Returns:
            Dicionário com análise e recomendações
        """
        
        # Extrair dados do cliente
        engajamento = cliente_data.get('pontuacao_engajamento', 0)
        assinante_clube = cliente_data.get('assinante_clube', False)
        cancelou = cliente_data.get('cancelou_assinatura', False)
        total_gasto = cliente_data.get('total_gasto', 0)
        n_compras = cliente_data.get('n_compras', 0)
        probabilidade_churn = cliente_data.get('probabilidade_churn', 0)
        
        # Inicializar resultado
        resultado = {
            'cliente_id': cliente_data.get('cliente_id'),
            'segmento': self._classificar_segmento(engajamento, assinante_clube, total_gasto),
            'nivel_engajamento': self._classificar_engajamento(engajamento),
            'probabilidade_churn': probabilidade_churn,
            'acoes_recomendadas': [],
            'prioridade': NivelPrioridade.BAIXA,
            'mensagem': '',
            'metricas': {
                'engajamento': engajamento,
                'total_gasto': total_gasto,
                'n_compras': n_compras,
                'probabilidade_churn': probabilidade_churn
            }
        }
        
        # Aplicar regras na ordem de prioridade
        regras_aplicadas = []
        
        # REGRA 1: Cliente Premium (Alta Engajamento + Assinante)
        if self._regra_cliente_premium(assinante_clube, engajamento):
            regras_aplicadas.append({
                'regra': 'REGRA_1_CLIENTE_PREMIUM',
                'condicao': f'assinante_clube=True E engajamento>={self.ENGAJAMENTO_ALTO}',
                'acao': AcaoRecomendada.VINHOS_PREMIUM,
                'descricao': 'Recomendar vinhos premium e rótulos exclusivos',
                'prioridade': NivelPrioridade.ALTA
            })
            regras_aplicadas.append({
                'regra': 'REGRA_1_CLIENTE_PREMIUM',
                'condicao': f'assinante_clube=True E engajamento>={self.ENGAJAMENTO_ALTO}',
                'acao': AcaoRecomendada.EVENTOS_EXCLUSIVOS,
                'descricao': 'Convidar para eventos e degustações VIP',
                'prioridade': NivelPrioridade.ALTA
            })
        
        # REGRA 2: Risco de Cancelamento (Cancelou + Baixo Engajamento)
        if self._regra_risco_cancelamento(cancelou, engajamento):
            regras_aplicadas.append({
                'regra': 'REGRA_2_RISCO_CANCELAMENTO',
                'condicao': f'cancelou=True E engajamento<{self.ENGAJAMENTO_BAIXO}',
                'acao': AcaoRecomendada.CUPOM_REATIVACAO,
                'descricao': f'Enviar cupom de {int(self.DESCONTO_REATIVACAO*100)}% de desconto',
                'prioridade': NivelPrioridade.CRITICA
            })
            regras_aplicadas.append({
                'regra': 'REGRA_2_RISCO_CANCELAMENTO',
                'condicao': f'cancelou=True E engajamento<{self.ENGAJAMENTO_BAIXO}',
                'acao': AcaoRecomendada.PESQUISA_SATISFACAO,
                'descricao': 'Enviar pesquisa de motivo de cancelamento',
                'prioridade': NivelPrioridade.CRITICA
            })
        
        # REGRA 3: Oportunidade de Upgrade (Médio Engajamento + Várias Compras)
        if self._regra_oportunidade_upgrade(engajamento, n_compras):
            regras_aplicadas.append({
                'regra': 'REGRA_3_OPORTUNIDADE_UPGRADE',
                'condicao': f'engajamento entre {self.ENGAJAMENTO_MEDIO_MIN} e {self.ENGAJAMENTO_MEDIO_MAX} E n_compras>{self.MIN_COMPRAS_FIDELIDADE}',
                'acao': AcaoRecomendada.UPGRADE_CLUBE,
                'descricao': 'Oferecer upgrade com frete grátis e benefícios',
                'prioridade': NivelPrioridade.MEDIA
            })
        
        # REGRA 4: Conversão para Clube (Não assinante + Alto Gasto)
        valor_medio_referencia = cliente_data.get('valor_medio_geral', 200)  # Valor de referência
        if self._regra_conversao_clube(assinante_clube, total_gasto, valor_medio_referencia):
            regras_aplicadas.append({
                'regra': 'REGRA_4_CONVERSAO_CLUBE',
                'condicao': f'não_assinante E total_gasto>{valor_medio_referencia}',
                'acao': AcaoRecomendada.ADESAO_CLUBE,
                'descricao': 'Recomendar adesão ao clube com simulação de economia',
                'prioridade': NivelPrioridade.ALTA
            })
        
        # REGRA 5: Alto Risco de Churn (Predição ML)
        if self._regra_alto_risco_churn(probabilidade_churn):
            regras_aplicadas.append({
                'regra': 'REGRA_5_ALTO_RISCO_CHURN',
                'condicao': f'probabilidade_churn>=0.7',
                'acao': AcaoRecomendada.CAMPANHA_REENGAJAMENTO,
                'descricao': 'Ativar campanha urgente de reengajamento',
                'prioridade': NivelPrioridade.CRITICA
            })
        
        # REGRA 6: Cliente Inativo (Poucas compras recentes)
        if self._regra_cliente_inativo(n_compras, engajamento):
            regras_aplicadas.append({
                'regra': 'REGRA_6_CLIENTE_INATIVO',
                'condicao': f'n_compras<=2 E engajamento<{self.ENGAJAMENTO_MEDIO_MIN}',
                'acao': AcaoRecomendada.PROGRAMA_FIDELIDADE,
                'descricao': 'Incluir em programa de fidelidade e reativação',
                'prioridade': NivelPrioridade.MEDIA
            })
        
        # Consolidar resultados
        if regras_aplicadas:
            resultado['acoes_recomendadas'] = regras_aplicadas
            resultado['prioridade'] = self._determinar_prioridade_maxima(regras_aplicadas)
            resultado['mensagem'] = self._gerar_mensagem(resultado['segmento'], regras_aplicadas)
        else:
            resultado['acoes_recomendadas'] = [{
                'regra': 'REGRA_DEFAULT',
                'condicao': 'nenhuma_condicao_especifica',
                'acao': AcaoRecomendada.NENHUMA,
                'descricao': 'Manter relacionamento padrão',
                'prioridade': NivelPrioridade.BAIXA
            }]
            resultado['mensagem'] = 'Cliente com comportamento estável. Manter estratégia atual.'
        
        return resultado
    
    # ========== REGRAS DE NEGÓCIO ==========
    
    def _regra_cliente_premium(self, assinante_clube: bool, engajamento: float) -> bool:
        """REGRA 1: Cliente Premium"""
        return assinante_clube and engajamento >= self.ENGAJAMENTO_ALTO
    
    def _regra_risco_cancelamento(self, cancelou: bool, engajamento: float) -> bool:
        """REGRA 2: Risco de Cancelamento"""
        return cancelou or engajamento < self.ENGAJAMENTO_BAIXO
    
    def _regra_oportunidade_upgrade(self, engajamento: float, n_compras: int) -> bool:
        """REGRA 3: Oportunidade de Upgrade"""
        return (self.ENGAJAMENTO_MEDIO_MIN <= engajamento <= self.ENGAJAMENTO_MEDIO_MAX 
                and n_compras > self.MIN_COMPRAS_FIDELIDADE)
    
    def _regra_conversao_clube(self, assinante_clube: bool, total_gasto: float, 
                               valor_medio: float) -> bool:
        """REGRA 4: Conversão para Clube"""
        return not assinante_clube and total_gasto > valor_medio
    
    def _regra_alto_risco_churn(self, probabilidade_churn: float) -> bool:
        """REGRA 5: Alto Risco de Churn"""
        return probabilidade_churn >= 0.7
    
    def _regra_cliente_inativo(self, n_compras: int, engajamento: float) -> bool:
        """REGRA 6: Cliente Inativo"""
        return n_compras <= 2 and engajamento < self.ENGAJAMENTO_MEDIO_MIN
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _classificar_segmento(self, engajamento: float, assinante_clube: bool, 
                             total_gasto: float) -> str:
        """Classifica o cliente em segmentos de negócio"""
        if assinante_clube and engajamento >= self.ENGAJAMENTO_ALTO:
            return "VIP Premium"
        elif assinante_clube:
            return "Clube Ativo"
        elif total_gasto > 250 and engajamento >= self.ENGAJAMENTO_MEDIO_MIN:
            return "Alto Valor"
        elif engajamento < self.ENGAJAMENTO_BAIXO:
            return "Em Risco"
        else:
            return "Regular"
    
    def _classificar_engajamento(self, engajamento: float) -> str:
        """Classifica o nível de engajamento"""
        if engajamento >= self.ENGAJAMENTO_ALTO:
            return "Alto"
        elif engajamento >= self.ENGAJAMENTO_MEDIO_MIN:
            return "Médio"
        else:
            return "Baixo"
    
    def _determinar_prioridade_maxima(self, regras: List[Dict]) -> NivelPrioridade:
        """Determina a prioridade máxima entre as regras aplicadas"""
        prioridades = [r['prioridade'] for r in regras]
        
        if NivelPrioridade.CRITICA in prioridades:
            return NivelPrioridade.CRITICA
        elif NivelPrioridade.ALTA in prioridades:
            return NivelPrioridade.ALTA
        elif NivelPrioridade.MEDIA in prioridades:
            return NivelPrioridade.MEDIA
        else:
            return NivelPrioridade.BAIXA
    
    def _gerar_mensagem(self, segmento: str, regras: List[Dict]) -> str:
        """Gera mensagem descritiva baseada no segmento e regras"""
        n_acoes = len(regras)
        
        if segmento == "VIP Premium":
            return f"Cliente VIP com {n_acoes} oportunidade(s) de aprofundamento do relacionamento."
        elif segmento == "Em Risco":
            return f"⚠️ Cliente em risco! {n_acoes} ação(ões) urgente(s) recomendada(s)."
        elif segmento == "Alto Valor":
            return f"Cliente de alto valor com {n_acoes} oportunidade(s) de conversão."
        else:
            return f"{n_acoes} ação(ões) recomendada(s) para melhorar engajamento."


# Instância global do motor de regras
rule_engine = RuleEngine()
