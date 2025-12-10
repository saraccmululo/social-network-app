document.addEventListener("DOMContentLoaded", ()=>{
  document.querySelectorAll(".btn-like").forEach(button=>{
    button.addEventListener("click", async ()=>{
      const postId = button.dataset.id;

      try{
        const response = await fetch(`/toggle_like/${postId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" }
        });

        if(!response.ok) {
        throw new Error("Network response was not ok");
        }
        const data = await response.json();

        // Find the heart and like-count span in the button
        const heart= button.querySelector(".heart-icon");
        
        if(heart) {
          heart.textContent=data.liked? "❤️":"🤍";
        }

        let likeCount= button.querySelector(".like-count");

        if (data.likes_count>0){
          // If the span doesn't exist yet, create it
          if (!likeCount) {
            likeCount=document.createElement("span");
            likeCount.className="like-count";
            button.appendChild(likeCount);
          }
          likeCount.textContent=data.likes_count;
        } else {
          //Remove span if count =0
          if(likeCount) likeCount.remove();
        }
      } catch (error) {
        console.error("Error liking/unliking post:", error);
      }
    });
  });
});