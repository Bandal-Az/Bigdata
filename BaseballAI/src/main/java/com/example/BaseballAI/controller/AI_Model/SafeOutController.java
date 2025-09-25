package com.example.BaseballAI.controller.AI_Model;

import com.example.BaseballAI.dto.AI_Model.SafeOutResponseDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.util.Map;

@CrossOrigin(origins = "http://localhost:3000", allowCredentials = "true")
@RestController
@RequestMapping("/upload_image")
public class SafeOutController {

    @Autowired
    private WebClient.Builder webClientBuilder;

    @PostMapping
    public SafeOutResponseDTO predict(@RequestParam("file") MultipartFile file) {
        try {
            if (file.isEmpty()) {
                return new SafeOutResponseDTO("error",
                        Map.of("message", "파일이 없습니다."));
            }

            final String originalFilename = file.getOriginalFilename() != null ? file.getOriginalFilename() : "tempfile.jpg";
            byte[] fileBytes = file.getBytes();

            // ByteArrayResource로 multipart 생성
            ByteArrayResource resource = new ByteArrayResource(fileBytes) {
                @Override
                public String getFilename() {
                    return originalFilename;
                }
            };

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", resource);

            Map<String, Object> response = webClientBuilder.baseUrl("http://localhost:8000")
                    .build()
                    .post()
                    .uri("/safe_out_api")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(body))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            String prediction = (String) response.get("prediction");
            String imageUrl = "/preview/" + originalFilename; // 미리보기 URL

            return new SafeOutResponseDTO(prediction,
                    Map.of("source", "Flask API", "imageUrl", imageUrl));

        } catch (WebClientResponseException e) {
            e.printStackTrace();
            return new SafeOutResponseDTO("error",
                    Map.of("message", "API 호출 실패: " + e.getMessage()));
        } catch (Exception e) {
            e.printStackTrace();
            return new SafeOutResponseDTO("error",
                    Map.of("message", "파일 처리 실패: " + e.getMessage()));
        }
    }
}
