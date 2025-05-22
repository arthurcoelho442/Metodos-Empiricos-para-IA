library("rstan") 

fit <- stan_model('hello_world.stan') 

stan(file = 'hello_world.stan',algorithm="Fixed_param")