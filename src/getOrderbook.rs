use reqwest::header::{HeaderMap, HeaderValue};
use serde_json::Value;
use std::time::Instant;
use dotenv::dotenv;
use std::env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();

    let client = reqwest::Client::new();
    
    let mut headers = HeaderMap::new();
    
    headers.insert("accept", HeaderValue::from_static("*/*"));
    headers.insert("accept-language", HeaderValue::from_static("en"));
    headers.insert("appid", HeaderValue::from_static("in.probo.pro"));
    headers.insert("authorization", HeaderValue::from_str(&format!("Bearer {}", env::var("PROBO_BEARER_TOKEN")?)).unwrap());
    headers.insert("content-type", HeaderValue::from_static("application/json"));

    let start_time = Instant::now();

    let response = client
        .get("https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId=3752921")
        .headers(headers)
        .send()
        .await?;
    
    let _data: Value = response.json().await?;
    
    let duration = start_time.elapsed();
    println!("Request took: {:?}", duration);
    
    // println!("{:#?}", data);
    
    Ok(())
} 