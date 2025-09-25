package com.example.BaseballAI.repository;

import com.example.BaseballAI.domain.NewsItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NewsItemRepository extends JpaRepository<NewsItem, Long> {
    // 필요하면 커스텀 쿼리 메소드 추가 가능
}