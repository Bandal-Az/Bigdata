package com.example.BaseballAI.dto.AI_Model;

import java.util.Map;

public class SafeOutResponseDTO {

    private String result;  // "safe" 또는 "out"
    private Map<String, Object> details;  // 부가 정보

    // Constructor
    public SafeOutResponseDTO(String result, Map<String, Object> details) {
        this.result = result;
        this.details = details;
    }

    // Getters and Setters
    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public Map<String, Object> getDetails() {
        return details;
    }

    public void setDetails(Map<String, Object> details) {
        this.details = details;
    }
}
