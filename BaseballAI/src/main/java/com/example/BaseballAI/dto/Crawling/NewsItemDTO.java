package com.example.BaseballAI.dto.Crawling;

import lombok.Data;

@Data
public class NewsItemDTO {
    private String title;
    private String url;
    private String date; // null 가능하니까 String으로 둬도 충분
}
