import React, { useEffect, useState } from "react";

export default function ReviewsPage() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/reviews`)
      .then(r => r.json())
      .then(setReviews);
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Local Business Reviews</h2>
      {reviews.map(rev => (
        <div key={rev.id} className="p-2 border-b mb-2">
          <strong>{rev.business_name}</strong> <br />
          Rating: {rev.rating} <br />
          {rev.comment}
        </div>
      ))}
      {/* Form for posting reviews can be added here */}
    </div>
  );
}
