// document.addEventListener("DOMContentLoaded", function () {
//     showCategory('today');
// });

// // function showCategory(category){
// //     document.querySelectorAll('.category-section').forEach(section => {
// //         section.style.display = 'none';
// //     });

// //     document.getElementById(category).style.display = 'block';
// // }

// function showCategory(category){
//     if (document.querySelectorAll('.category-section.past').forEach(section => {
//         section.style.display = 'none';
//     }));
// }

document.addEventListener("DOMContentLoaded", function () {
    showCategory('today'); // 기본값: 오늘의 편지 보이기
});

function showCategory(category) {
    // 모든 편지 리스트 숨김 처리
    document.querySelectorAll('.category').forEach(el => {
        el.classList.remove('active');
    });

    // 선택된 카테고리만 보이도록 설정
    document.getElementsByClassName(category).classList.add('active');
}

document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".btn"); // 햄버거 버튼
    const menu = document.getElementById("menu"); // 사이드 메뉴
    const pageCover = document.querySelector(".page_cover"); // 배경 어두워지는 영역

    // 햄버거 버튼 클릭 시 메뉴 열기
    menuButton.addEventListener("click", function () {
        document.documentElement.classList.toggle("open");
        menu.classList.toggle("open");
        pageCover.classList.toggle("open");
    });

    // 메뉴 바깥 클릭 시 닫기
    pageCover.addEventListener("click", function () {
        document.documentElement.classList.remove("open");
        menu.classList.remove("open");
        pageCover.classList.remove("open");
    });
});

function toggleDateOptions() {
    var routineType = document.getElementById("routine_type").value;
    document.getElementById("weekly-options").style.display = (routineType === "weekly") ? "block" : "none";
    document.getElementById("monthly-options").style.display = (routineType === "monthly") ? "block" : "none";
}

function setMood(mood){
    alert("오늘의 기분이 '${mood}'로 설정되었습니다. 편지를 작성해보세요!");
}

document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tabs li");
    const tabContents = document.querySelectorAll("[data-tab-content]");
    // 초기 상태: "오늘의 편지"만 보이게 설정
    tabContents.forEach(content => content.classList.remove("active"));
    document.querySelector("#today").classList.add("active");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const targetId = tab.getAttribute("data-tab-target");
            const targetContent = document.querySelector(targetId);
            
            if (!targetContent) {
                console.error("탭 콘텐츠를 찾을 수 없습니다:", targetId);
                return;
            }

            // 모든 탭 버튼에서 active 클래스 제거
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            // 모든 탭 콘텐츠 숨김
            tabContents.forEach(content => content.classList.remove("active"));
            targetContent.classList.add("active");
        });
    });
});
