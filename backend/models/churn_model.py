"""
Modelo de Machine Learning para Predição de Churn
Implementa Random Forest para classificação de cancelamento
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, classification_report, confusion_matrix
)
import joblib
from pathlib import Path
from typing import Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')


class ChurnPredictor:
    """Modelo de predição de churn (cancelamento)"""
    
    def __init__(self, model_type='random_forest'):
        """
        Inicializa o preditor de churn
        
        Args:
            model_type: Tipo de modelo ('random_forest', 'decision_tree', 'logistic')
        """
        self.model_type = model_type
        self.model = None
        self.label_encoders = {}
        self.feature_names = []
        self.feature_importance = None
        
    def prepare_features(self, df: pd.DataFrame, target_col='cancelou_assinatura') -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepara features para o modelo
        
        Args:
            df: DataFrame com dados dos clientes
            target_col: Nome da coluna alvo
            
        Returns:
            X (features), y (target)
        """
        
        # Selecionar features relevantes
        feature_columns = [
            'pontuacao_engajamento',
            'total_gasto',
            'n_compras',
            'ticket_medio',
            'idade',
            'assinante_clube',
            'cidade'
        ]
        
        # Filtrar apenas colunas existentes
        available_features = [col for col in feature_columns if col in df.columns]
        
        # Criar cópia do dataframe
        df_model = df[available_features + [target_col]].copy()
        
        # Remover linhas com valores nulos
        df_model = df_model.dropna()
        
        # Encoding de variáveis categóricas
        for col in df_model.select_dtypes(include=['object']).columns:
            if col != target_col:
                le = LabelEncoder()
                df_model[col] = le.fit_transform(df_model[col].astype(str))
                self.label_encoders[col] = le
        
        # Encoding do target (se for string)
        if df_model[target_col].dtype == 'object':
            le_target = LabelEncoder()
            df_model[target_col] = le_target.fit_transform(df_model[target_col])
            self.label_encoders[target_col] = le_target
        
        # Separar features e target
        X = df_model.drop(columns=[target_col])
        y = df_model[target_col]
        
        self.feature_names = list(X.columns)
        
        return X, y
    
    def train(self, X: pd.DataFrame, y: pd.Series, test_size=0.2, random_state=42):
        """
        Treina o modelo
        
        Args:
            X: Features
            y: Target
            test_size: Proporção de dados para teste
            random_state: Seed para reprodutibilidade
        """
        
        # Split dos dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Selecionar e treinar modelo
        if self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=random_state,
                class_weight='balanced'
            )
        elif self.model_type == 'decision_tree':
            self.model = DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=random_state,
                class_weight='balanced'
            )
        elif self.model_type == 'logistic':
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=random_state,
                class_weight='balanced'
            )
        
        # Treinar
        self.model.fit(X_train, y_train)
        
        # Calcular importância das features (se disponível)
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        
        # Avaliar
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred, zero_division=0)
        }
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Faz predições
        
        Args:
            X: Features
            
        Returns:
            Array com predições (0 ou 1)
        """
        if self.model is None:
            raise ValueError("Modelo não treinado. Execute train() primeiro.")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Faz predições com probabilidades
        
        Args:
            X: Features
            
        Returns:
            Array com probabilidades [prob_classe_0, prob_classe_1]
        """
        if self.model is None:
            raise ValueError("Modelo não treinado. Execute train() primeiro.")
        
        return self.model.predict_proba(X)
    
    def save_model(self, filepath: str):
        """Salva o modelo treinado"""
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'model_type': self.model_type
        }
        joblib.dump(model_data, filepath)
        print(f"✅ Modelo salvo em: {filepath}")
    
    @classmethod
    def load_model(cls, filepath: str):
        """Carrega um modelo treinado"""
        model_data = joblib.load(filepath)
        
        predictor = cls(model_type=model_data['model_type'])
        predictor.model = model_data['model']
        predictor.label_encoders = model_data['label_encoders']
        predictor.feature_names = model_data['feature_names']
        predictor.feature_importance = model_data.get('feature_importance')
        
        print(f"✅ Modelo carregado de: {filepath}")
        return predictor


def train_churn_model():
    """Função principal para treinar o modelo de churn"""
    
    print("\n" + "=" * 60)
    print("🤖 TREINAMENTO DO MODELO DE CHURN")
    print("=" * 60)
    
    # Caminhos
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data" / "processed"
    MODEL_DIR = BASE_DIR / "data" / "models"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Carregar dados
    print("\n📂 Carregando dados...")
    df = pd.read_csv(DATA_DIR / "clientes_agregado.csv")
    print(f"✅ {len(df)} clientes carregados")
    
    # Treinar múltiplos modelos
    models = ['random_forest', 'decision_tree', 'logistic']
    results = {}
    
    for model_type in models:
        print(f"\n{'='*60}")
        print(f"🔬 Treinando modelo: {model_type.upper()}")
        print(f"{'='*60}")
        
        # Inicializar preditor
        predictor = ChurnPredictor(model_type=model_type)
        
        # Preparar features
        X, y = predictor.prepare_features(df)
        print(f"\n📊 Features: {list(X.columns)}")
        print(f"📊 Target distribution:\n{y.value_counts()}")
        
        # Treinar
        metrics = predictor.train(X, y)
        
        # Exibir resultados
        print(f"\n📈 Métricas do Modelo:")
        print(f"  • Acurácia: {metrics['accuracy']:.4f}")
        print(f"  • Precisão: {metrics['precision']:.4f}")
        print(f"  • Recall: {metrics['recall']:.4f}")
        print(f"  • F1-Score: {metrics['f1_score']:.4f}")
        
        # Importância das features
        if predictor.feature_importance is not None:
            print(f"\n🎯 Importância das Features:")
            print(predictor.feature_importance.to_string(index=False))
        
        # Salvar modelo
        model_path = MODEL_DIR / f"churn_model_{model_type}.pkl"
        predictor.save_model(str(model_path))
        
        results[model_type] = {
            'predictor': predictor,
            'metrics': metrics,
            'model_path': model_path
        }
    
    # Selecionar melhor modelo
    best_model_type = max(results, key=lambda x: results[x]['metrics']['f1_score'])
    best_predictor = results[best_model_type]['predictor']
    
    print(f"\n{'='*60}")
    print(f"🏆 Melhor Modelo: {best_model_type.upper()}")
    print(f"   F1-Score: {results[best_model_type]['metrics']['f1_score']:.4f}")
    print(f"{'='*60}")
    
    # Salvar melhor modelo como padrão
    default_path = MODEL_DIR / "churn_model.pkl"
    best_predictor.save_model(str(default_path))
    
    print("\n✨ Treinamento concluído com sucesso! ✨\n")
    
    return results


if __name__ == "__main__":
    train_churn_model()
