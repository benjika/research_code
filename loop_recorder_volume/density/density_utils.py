def compute_density(volume_in_liters, weight_in_kg,position_id):
	density_kg_to_cubic_meter = weight_in_kg * (1000 / volume_in_liters)
	print(f'Measured feed density position {position_id}: {density_kg_to_cubic_meter} Kg in cubic meter')
	return density_kg_to_cubic_meter