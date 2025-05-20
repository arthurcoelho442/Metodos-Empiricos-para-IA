library(rstan)

# Compilar o modelo Stan
model <- stan_model(file = "hello_world.stan")

# Rodar a amostragem
fit <- sampling(model, data = list(), iter = 1000, chains = 4)

# Exibir resultados
print(fit)
plot(fit)
