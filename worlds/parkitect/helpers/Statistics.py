from ..data.item_info import item_info

# Helper Class to have a structure for randomization
class Statistics:
  def __init__(
    self,
    name,
    amount = 0,
    excitement = 0,
    intensity = 0,
    nausea = 0,
    satisfaction = 0,
    revenue = 0,
    customers = 0,
  ):
    is_shop = name in item_info["Shops"]
    is_ride = name in item_info["Rides"]
    is_coaster = name in item_info["Coaster Rides"]
    is_trap = name in item_info['trap_items']

    self.name = name
    self.amount = amount
    self.excitement = excitement
    self.intensity = intensity
    self.nausea = nausea
    self.satisfaction = satisfaction
    self.revenue = revenue
    self.customers = customers

    # its a category
    if not is_shop and not is_ride and not is_coaster and not is_trap:
      self.type = name
      self.name = ""

    else:
      self.type = "shop" if is_shop else "coaster" if is_coaster else "ride" if is_ride else "trap" if is_trap else "unknown"

  def to_dict(self):

    if self.type == 'coaster':
      return {
        "name": self.name,
        "amount": self.amount,
        "excitement": self.excitement,
        "intensity": self.intensity,
        "nausea": self.nausea,
        "satisfaction": self.satisfaction,
        "revenue": self.revenue,
        "customers": self.customers,
        "type": self.type,
      }

    if self.type == 'shop' or self.type == 'ride' or self.type in item_info["shop_types"] or self.type in item_info["ride_types"]:
      return {
        "name": self.name,
        "amount": self.amount,
        "revenue": self.revenue,
        "customers": self.customers,
        "type": self.type,
      }

    if self.type == 'trap':
      return {
        "name": self.name,
        "amount": self.amount,
        "type": self.type,
      }

    #something went wrong here :D item not in item_info?
    print('----------------- !!! ----------------')
    print({
        "name": self.name,
        "amount": self.amount,
        "type": self.type,
      })
    print('----------------- !!! ----------------')


  @staticmethod
  def random_roll(name: str, amount: int, rule, possible_prereqs = [], force = False):
    """
    Creates and returns a new Statistics object with randomly generated values.
    """
    option_excitement = 0
    option_intensity = 0
    option_nausea = 0 
    option_satisfaction = 0 
    option_revenue = 0
    option_total_customers = 0

    max_excitement = rule.options.challenge_maximum_excitement.value
    max_intensity = rule.options.challenge_maximum_intensity.value
    max_nausea = rule.options.challenge_maximum_nausea.value
    max_satisfaction = rule.options.challenge_maximum_satisfaction.value
    max_ride_revenue = rule.options.challenge_maximum_ride_revenue.value
    max_shop_revenue = rule.options.challenge_maximum_shop_revenue.value
    max_customers = rule.options.challenge_customers.value

    if name in item_info["Coaster Rides"] or name == "Coaster Rides":
      if rule.random.random() < .5 and max_excitement > 0:
        option_excitement = 0 if max_excitement <= 0 else round(rule.random.uniform(0, max_excitement))

      if rule.random.random() < .5 and max_intensity > 0:
        option_intensity = 0 if max_intensity <= 0 else round(rule.random.uniform(0, max_intensity))

      if rule.random.random() < .5 and max_nausea > 0:
        option_nausea = 0 if max_nausea <= 0 else round(rule.random.uniform(0, max_nausea))

      if rule.random.random() < .5 and max_satisfaction > 0:
        option_satisfaction = 0 if max_satisfaction <= 0 else round(rule.random.uniform(0, max_satisfaction))

    # Helps less good stat Coaster to reach it easier
    if name in item_info["stat_exempt_coaster_rides"] or any(item in item_info["stat_exempt_coaster_rides"] for item in possible_prereqs):
      if max_excitement >= 15:
        option_excitement = min(15, option_excitement * 0.33)
      if max_intensity >= 15:
        option_intensity = min(15, option_intensity * 0.33)
    
        option_nausea = 0
        option_satisfaction = option_satisfaction * .5

    if name in item_info["Rides"] or name == "Rides":
      if rule.random.random() < .5:
        option_revenue = round(rule.random.uniform(0, max_ride_revenue))

    elif (name in item_info["Shops"] and name not in item_info['non_profitables']) or (name == "Shops" and any(item not in item_info["non_profitables"] for item in possible_prereqs)):
      if rule.random.random() < .5:
        option_revenue = round(rule.random.uniform(0, max_shop_revenue))

      if name in item_info['stat_exempt_shops'] and option_revenue > 500:
        option_revenue = round(rule.random.uniform(200, 500))

    if name not in item_info['trap_items']:
      if rule.random.random() < .5:
        option_total_customers = round(rule.random.uniform(0, max_customers))

      no_stats = option_excitement == 0 and option_intensity == 0 and option_nausea == 0 and option_revenue == 0 and option_total_customers == 0

      if no_stats and (rule.random.random() < .85 or force):
        option_total_customers = round(rule.random.uniform(0, max_customers))

    # Create and return a new Statistics object
    return Statistics(
      name = name,
      amount = amount,
      excitement = option_excitement,
      intensity = option_intensity,
      nausea = option_nausea,
      satisfaction = option_satisfaction,
      revenue = option_revenue,
      customers = option_total_customers,
    )
  