#include <iostream>
#include <string>
#include <curl/curl.h>
#include <chrono>
#include <fstream> 
// Callback function to capture response
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

void makeFirstRequest() {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string responseString;

        curl_easy_setopt(curl, CURLOPT_URL, "https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId=3362847");

        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "authorization: Bearer emA04yGrGFvf9mIPsyoIXaOLtfyEohW5Af4WjWmFfQI=");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "First request cURL error: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "First request response: " << responseString << std::endl;

            // Save the JSON response to a file
            std::ofstream outFile("response.json");
            if (outFile.is_open()) {
                outFile << responseString;
                outFile.close();
                std::cout << "Response saved to response.json" << std::endl;
            } else {
                std::cerr << "Error opening file to write response." << std::endl;
            }
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
}
// Function to make the second request
void makeSecondRequest() {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string responseString;

        curl_easy_setopt(curl, CURLOPT_URL, "https://prod.api.probo.in/api/v1/product/public/arena/events");

        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "authorization: Bearer emA04yGrGFvf9mIPsyoIXaOLtfyEohW5Af4WjWmFfQI=");
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, R"({"page":1,"limit":15,"sortType":"","filter":{},"topicIds":[2449]})");

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Second request cURL error: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "Second request response: " << responseString << std::endl;
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
}

int main() {
    // Initialize curl globally
    curl_global_init(CURL_GLOBAL_DEFAULT);

    // Make the first request
    auto start = std::chrono::high_resolution_clock::now();

    makeFirstRequest();

    // End time
    auto end = std::chrono::high_resolution_clock::now();

    // Calculate duration
    std::chrono::duration<double> duration = end - start;

    // Output the time taken
    std::cout << "Time taken: " << duration.count() << " seconds." << std::endl;

    // Make the second request
    // makeSecondRequest();

    // Cleanup global curl resources
    curl_global_cleanup();
    return 0;
}
