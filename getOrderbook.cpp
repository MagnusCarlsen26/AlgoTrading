#include <iostream>
#include <string>
#include <chrono>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <cstdlib> // for getenv

// Callback function for writing response data from curl
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t total_size = size * nmemb;
    response->append((char*)contents, total_size);
    return total_size;
}

int main() {
    // Start timing
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Get bearer token from environment variable
    const char* bearer_token = std::getenv("PROBO_BEARER_TOKEN");
    if (!bearer_token) {
        std::cerr << "Error: PROBO_BEARER_TOKEN environment variable not set" << std::endl;
        return 1;
    }
    
    // Initialize curl
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "Error initializing curl" << std::endl;
        return 1;
    }
    
    // Response string
    std::string response_data;
    
    // Prepare headers
    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "accept: */*");
    headers = curl_slist_append(headers, "accept-language: en");
    headers = curl_slist_append(headers, "appid: in.probo.pro");
    
    // Create authorization header with bearer token
    std::string auth_header = "authorization: Bearer " + std::string(bearer_token);
    headers = curl_slist_append(headers, auth_header.c_str());
    headers = curl_slist_append(headers, "content-type: application/json");
    
    // Set curl options
    curl_easy_setopt(curl, CURLOPT_URL, "https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId=3752921");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);
    
    // Perform the request
    CURLcode res = curl_easy_perform(curl);
    
    // Check for errors
    if (res != CURLE_OK) {
        std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
        return 1;
    }
    
    // Calculate duration
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count() / 1000.0;
    
    // Print timing information
    std::cout << "Request took: " << duration << " milliseconds" << std::endl;
    
    // Parse and use JSON data if needed
    try {
        nlohmann::json json_data = nlohmann::json::parse(response_data);
        // Uncomment to print the JSON data
        // std::cout << json_data.dump(4) << std::endl;
    } catch (const nlohmann::json::exception& e) {
        std::cerr << "JSON parsing error: " << e.what() << std::endl;
    }
    
    // Clean up
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);
    
    return 0;
}
