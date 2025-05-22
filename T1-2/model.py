import os
from cmdstanpy import CmdStanModel

model = os.path.join('./model.stan')
data  = os.path.join('./data.json')

# Compile example model model.stan
model = CmdStanModel(stan_file=model)

# Condition on example data model.data.json
# Condition on example data data.json
fit = model.sample(
    fixed_param=True
)

print(fit.summary())  # resumo estatístico dos parâmetros

for i, stdout_file in enumerate(fit.runset.stdout_files, start=1):
    with open(stdout_file) as f:
        print(f.read())
