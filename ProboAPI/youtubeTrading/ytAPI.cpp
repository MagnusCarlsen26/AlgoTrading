#include <iostream>
#include <string>
#include <curl/curl.h>
#include <cstdlib> // for std::getenv
#include <ctime>

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

int main() {
    // Get the API key from environment variables
    const char* api_key = "AIzaSyAvNVx0GmlNXcJ4cexGUsjQ-VnaEDImTpg";
    if (!api_key) {
        std::cerr << "Error: YT_API_2 environment variable not set." << std::endl;
        return 1;
    }

    std::string video_id = "YOUR_VIDEO_ID"; // Replace with the actual video ID
    std::string readBuffer;

    // Construct the URL
    std::string url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" + video_id + "&key=" + api_key;

    // Measure the time taken for the request
    auto start = std::clock();

    // Initialize CURL
    CURL* curl;
    CURLcode res;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
        // Perform the request
        res = curl_easy_perform(curl);
        // Check for errors
        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        // Clean up
        curl_easy_cleanup(curl);
    }

    auto end = std::clock();

    // Print the response
    std::cout << "Response: " << readBuffer << std::endl;
    std::cout << "Time taken: " << (end - start) / (double)CLOCKS_PER_SEC << " seconds" << std::endl;

    return 0;
}
