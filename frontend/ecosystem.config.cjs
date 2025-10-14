module.exports = {
  apps: [
    {
      name: "printlabel-frontend",
      script: "npm",
      args: "run preview",
      cwd: "./",
      env: {
        NODE_ENV: "production",
        PORT: 3002
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 3002
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      restart_delay: 4000,
      log_file: "./logs/app.log",
      out_file: "./logs/out.log",
      error_file: "./logs/error.log",
      merge_logs: true,
      time: true
    }
  ]
};