declare namespace NodeJS {
    interface ProcessEnv {
        DB_URI: string
        JWT_SECRET: string
        SMTP_MAIL: string,
        SMTP_PASS: string,
        NODE_ENV: "development" | "production" | "test",
        CLIENT_URL: string,
        PORT: string,
        CLOUD_NAME: string,
        CLOUD_API_KEY: string,
        CLOUD_API_SECRET: string,
        AI_API_BASE_URL: string
    }
}