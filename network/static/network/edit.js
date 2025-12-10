
const editMode =(postId, button)=> {
  const p = document.querySelector(`#post-content-${postId}`)

  //Create new textarea pre-filled with text
  const textarea= document.createElement('textarea');
  textarea.className="form-control";
  textarea.value= p.innerText;

  //replace paragraph with textarea
  p.replaceWith(textarea);

  //change button name from 'edit' to 'save'
  button.textContent="💾";

  //change button behavior to save
  button.onclick=()=> saveEdit(postId, button, textarea,);
};
  

const saveEdit = async (postId, button, textarea)=>{
  try{
  //get the new text
    const newText=textarea.value

    //send it to backend
    const response = await fetch(`/edit/${postId}`, {
      method:"PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: newText
      })
    });
    if(!response.ok) {
      throw new Error("Failed to save post");
    }

    const data = response.json();

    //create a new p element
    const p = document.createElement('p');
    p.id=`post-content-${postId}`;
    p.innerText=newText;

    //Replace textarea with p new text
    textarea.replaceWith(p);

    //Restore button to "Edit"
    button.textContent="📝";

    //Restore original button behavior
    button.onclick=()=> editMode(postId, button);
    
  } catch (error) {
    console.error("Error saving post:", error);
  }
};


document.addEventListener("DOMContentLoaded", ()=>{
  document.querySelectorAll('.edit-btn').forEach(button=>{
    //get post id
    const postId=button.dataset.id;
    button.onclick=()=> editMode(postId, button);
    });
  });