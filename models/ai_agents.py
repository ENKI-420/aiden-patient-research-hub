from mesa import Agent, Model

class MutationRiskAgent(Agent):
    def __init__(self, unique_id, model, mutation_data):
        super().__init__(unique_id, model)
        self.mutation_data = mutation_data
        self.risk_score = 0

    def step(self):
        self.risk_score = sum([mutation["pathogenicity_score"] for mutation in self.mutation_data])
        return self.risk_score

class MultiAgentRiskModel(Model):
    def __init__(self, num_agents, mutation_data):
        self.num_agents = num_agents
        self.mutation_data = mutation_data
        self.agents = [MutationRiskAgent(i, self, mutation_data) for i in range(num_agents)]

    def run_model(self):
        total_risk = sum(agent.step() for agent in self.agents)
        return total_risk / self.num_agents