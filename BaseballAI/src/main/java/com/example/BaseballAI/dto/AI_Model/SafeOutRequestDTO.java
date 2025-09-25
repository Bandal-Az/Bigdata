package com.example.BaseballAI.dto.AI_Model;

import org.springframework.web.multipart.MultipartFile;

public class SafeOutRequestDTO {

        private MultipartFile imageFile;  // 사진 파일을 받는 필드

        // Constructor
        public SafeOutRequestDTO(MultipartFile imageFile) {
            this.imageFile = imageFile;
        }

        // Getter and Setter
        public MultipartFile getImageFile() {
            return imageFile;
        }

        public void setImageFile(MultipartFile imageFile) {
            this.imageFile = imageFile;
        }
}
