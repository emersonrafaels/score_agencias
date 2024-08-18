from pydantic import BaseModel, root_validator, ValidationError
from typing import Optional


class ConsumoEnergiaModel(BaseModel):
	ice: Optional[float] = None
	percentual_acima: Optional[float] = None

	@root_validator(pre=True)
	def check_ice_or_percentual(cls, values):
		ice = values.get('ice')
		percentual_acima = values.get('percentual_acima')

		# Verifica se ambos os valores foram fornecidos ou se nenhum foi fornecido
		if ice is not None and percentual_acima is not None:
			raise ValueError(
				"Você deve fornecer apenas 'ice' ou 'percentual_acima', não ambos.")
		elif ice is None and percentual_acima is None:
			raise ValueError("Você deve fornecer 'ice' ou 'percentual_acima'.")

		return values


class ConsumoEnergia:
	def __init__(self, ice=None, percentual_acima=None):

		# VALIDANDO OS DADOS COM O MODELO DO PYDANTIC
		model = ConsumoEnergiaModel(ice=ice, percentual_acima=percentual_acima)

		# INICIANDO AS VARIÁVEIS APÓS A VALIDAÇÃO
		self.ice = model.ice
		self.percentual_acima = model.percentual_acima

	def calcular_percentual(self):
		"""
			Calcula o percentual acima do ideal baseado no ICE.
		"""
		if self.ice >= 1:
			return (self.ice - 1) * 100
		return 0

	def calcular_ice(self):
		"""
			Calcula o ICE baseado no percentual acima do ideal.
		"""
		return (self.percentual_acima / 100) + 1

	def __str__(self):
		"""
			Retorna a mensagem formatada ao converter a instância em string.
		"""
		if self.ice is not None:
			if self.ice >= 1:
				percentual = self.calcular_percentual()
				return f"O consumo está {percentual:.2f}% acima do ideal para um ICE de {self.ice:.2f}."
			else:
				return f"O consumo está dentro do ideal, com um ICE de {self.ice:.2f}."

		elif self.percentual_acima is not None:
			ice_calculado = self.calcular_ice()
			return f"Um consumo {self.percentual_acima}% acima do ideal corresponde a um ICE de {ice_calculado:.2f}."

		return "Você deve fornecer o valor de 'ice' ou 'percentual_acima'."

	def __call__(self):
		"""
			Permite que a instância seja chamada como uma função.
		"""
		return str(self)


if __name__ == '__main__':

	# Exemplo de uso:
	try:
		# Instância correta
		consumo1 = ConsumoEnergia(ice=2)
		print(consumo1())  # Usando o método mágico __call__

		# Instância com erro (ambos fornecidos)
		consumo2 = ConsumoEnergia(ice=2, percentual_acima=100)
	except ValidationError as e:
		print(e)

	try:
		# Instância com apenas percentual_acima fornecido
		consumo3 = ConsumoEnergia(percentual_acima=50)
		print(consumo3())  # Usando o método mágico __call__
	except ValidationError as e:
		print(e)
