data {
  int<lower=0> N; // Number of data points
  vector[N] y;    // Data
}
parameters {
  real mu;        // Mean
  real<lower=0> sigma; // Standard deviation
}
model {
  mu ~ normal(0, 10); // Prior for mean
  sigma ~ cauchy(0, 2.5); // Prior for standard deviation
  y ~ normal(mu, sigma); // Likelihood
}