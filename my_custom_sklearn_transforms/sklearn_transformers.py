from sklearn.base import BaseEstimator, TransformerMixin


# All sklearn Transforms must have the `transform` and `fit` methods
class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Primeiro realizamos a cópia do dataframe 'X' de entrada
        data = X.copy()
        # Retornamos um novo dataframe sem as colunas indesejadas
        return data.drop(labels=self.columns, axis='columns')


class ClipColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns, value):
        self.columns = columns
        self.value = value

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):        
        data = X.copy()
        for column in self.columns:
            data[column] = data.apply(lambda x: self.value if x[column]>self.value else x[column] , axis=1)
        return data

class AddMediaGeral(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):        
        data = X.copy()
        data['MEDIA'] = data.apply(lambda x: (x['NOTA_DE']+x['NOTA_EM']+x['NOTA_MF']+x['NOTA_GO'])/4 if x['NOTA_DE']+x['NOTA_EM']+x['NOTA_MF']+x['NOTA_GO']>0 else 0 , axis=1)
        return data

class FillNANSpecial(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Primeiro realizamos a cópia do dataframe 'X' de entrada
        data = X.copy()
        for field in ['DE','EM','MF','GO']:
            median = data['NOTA_'+field].median()
            data['NOTA_'+field] = data.apply(self.fillnan, args=(field, median), axis=1)
        return data
    
    def fillnan(self, row, field, median):
        #set nota_x with nan to median of go or 0 if reprovado_X > 0       
        if np.isnan(row['NOTA_'+field]):
            if row['REPROVACOES_'+field] > 0:
                return 0
            else:
                return median
        else:
            return row['NOTA_'+field]