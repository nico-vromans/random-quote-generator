"use client";

import React, { useEffect, useState } from "react";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { ModeToggle } from "@/components/ui/mode-toggle";
import { BackgroundGradient } from "@/components/ui/background-gradient";
import { Badge } from "@/components/ui/badge"
import { FaThumbsUp, FaRegThumbsUp, FaThumbsDown, FaRegThumbsDown } from "react-icons/fa6";
import { cn } from "@/lib/utils";

export default function Home() {
  const baseQuotesUrl = 'http://0.0.0.0:8000/quotes/';

  function getPreviousVote(guid: string) {
    const interaction = localStorage.getItem(guid);

    if (interaction !== null) {
      return interaction;
    }

    return null;
  }

  const [quoteData, setQuoteData] = useState(null); // State to hold quote data
  const [loading, setLoading] = useState(true); // Loading state

  const likeQuote = async () => {
    let response;
    let queryParams;
    const previousVote = getPreviousVote(guid);


    if (!previousVote) {
      localStorage.setItem(guid, 'like');
      queryParams = new URLSearchParams({ direction: 'increase' })
      response = await fetch(baseQuotesUrl + guid + "/like/?" + queryParams.toString(), { method: "PATCH" });
    } else {
      if (previousVote === 'like') {
        localStorage.removeItem(guid);
        queryParams = new URLSearchParams({ direction: 'decrease' })
        response = await fetch(baseQuotesUrl + guid + "/like/?" + queryParams.toString(), { method: "PATCH" });
      } else {
        localStorage.setItem(guid, 'like');
        queryParams = new URLSearchParams({ direction: 'increase', reverse_opposite: 'true' })
        response = await fetch(baseQuotesUrl + guid + "/like/?" + queryParams.toString(), { method: "PATCH" });
      }
    }

    const data = await response.json();
    const imageResponse = await Promise.resolve(
      fetch(data.image_url, { method: 'head' }).catch(() => null)
    );

    data.is_image_accessible = imageResponse?.ok || false;
    setQuoteData(data); // Save the data to state
  }

  const dislikeQuote = async () => {
    let response;
    let queryParams;
    const previousVote = getPreviousVote(guid);

    if (!previousVote) {
      localStorage.setItem(guid, 'dislike');
      queryParams = new URLSearchParams({ direction: 'increase' })
      response = await fetch(baseQuotesUrl + guid + "/dislike/?" + queryParams.toString(), { method: "PATCH" });
    } else {
      if (previousVote === 'dislike') {
        localStorage.removeItem(guid);
        queryParams = new URLSearchParams({ direction: 'decrease' })
        response = await fetch(baseQuotesUrl + guid + "/dislike/?" + queryParams.toString(), { method: "PATCH" });
      } else {
        localStorage.setItem(guid, 'dislike');
        queryParams = new URLSearchParams({ direction: 'increase', reverse_opposite: 'true' })
        response = await fetch(baseQuotesUrl + guid + "/dislike/?" + queryParams.toString(), { method: "PATCH" });
      }
    }

    const data = await response.json();
    const imageResponse = await Promise.resolve(
      fetch(data.image_url, { method: 'head' }).catch(() => null)
    );

    data.is_image_accessible = imageResponse?.ok || false;
    setQuoteData(data); // Save the data to state
  }

  useEffect(() => {
    // Fetching data from the Quote API
    const fetchQuotes = async () => {
      try {
        // TODO: continue with this functionality
        const response = await fetch(baseQuotesUrl + "get_random_quote/");
        const data = await response.json();
        const imageResponse = await Promise.resolve(
          fetch(data.image_url, { method: 'head' }).catch(() => null)
        );

        data.is_image_accessible = imageResponse?.ok || false;
        setQuoteData(data); // Save the data to state
      } catch (error) {
        console.error("Error fetching quote data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
  }, []);

  if (loading) return <p>Loading...</p>;

  if (!quoteData) return <p>No quote data.</p>;

  const {
    guid,
    author,
    quote_text,
    category,
    likes,
    dislikes,
    image_url,
    image_alt_text,
    is_image_accessible
  } = quoteData;

  return (
    <AuroraBackground>
      <div className="absolute top-10 right-10 z-50">
        <ModeToggle />
      </div>
      <div>
        <BackgroundGradient className="rounded-lg p-3 sm:p-10 bg-white dark:bg-zinc-900">
          <div
            className={cn(
              "overflow-hidden relative card min-h-80 w-[500px] rounded-lg backgroundImage p-4",
              { "shadow-xl": is_image_accessible }
            )}
            style={is_image_accessible ? {
              backgroundImage: `url(${image_url})`,
              backgroundSize: "cover",
              backgroundPosition: "center"
            } : {}}
          >
            {is_image_accessible && (
              <div className="backdrop-blur-sm absolute inset-0 bg-black bg-opacity-50 pointer-events-none"></div>
            )}
            <div className="flex flex-col justify-center">
              <p className={cn(
                "text-base sm:text-xl mt-4 mb-2 font-bold z-10",
                {
                  "text-neutral-50 dark:text-neutral-50": is_image_accessible,
                  "text-neutral-600 dark:text-neutral-50": !is_image_accessible,
                }
              )}>
                &quot;{quote_text}&quot;
              </p>
              <p className={cn(
                "text-sm italic z-10",
                {
                  "text-neutral-300 dark:text-neutral-300": is_image_accessible,
                  "text-neutral-400 dark:text-neutral-500": !is_image_accessible,
                }
              )}>
                {author['name']}
              </p>
            </div>
          </div>

          <div className="flex justify-between mt-12">
            <button onClick={likeQuote}
                    className={cn(
                      "px-6 py-2 bg-transparent border-2 dark:text-white text-black rounded-lg font-bold " +
                      "transform hover:-translate-y-1 transition duration-400",
                      { "border-green-700 dark:border-green-700": getPreviousVote(guid) === 'like' },
                      { "border-black dark:border-white": getPreviousVote(guid) !== 'like' },
                    )}>
              {getPreviousVote(guid) === 'like' ? <FaThumbsUp className="text-green-700" /> : <FaRegThumbsUp />}
              <span>{likes}</span>
            </button>
            <div className="align-middle content-center">
              <Badge>{category['name']}</Badge>
            </div>
            <button onClick={dislikeQuote}
                    className={cn(
                      "px-6 py-2 bg-transparent border-2 dark:text-white text-black rounded-lg font-bold " +
                      "transform hover:-translate-y-1 transition duration-400",
                      { "border-red-700 dark:border-red-700": getPreviousVote(guid) === 'dislike' },
                      { "border-black dark:border-white": getPreviousVote(guid) !== 'dislike' },
                    )}>
              {getPreviousVote(guid) === 'dislike' ? <FaThumbsDown className="text-red-700" /> : <FaRegThumbsDown />}
              <span>{dislikes}</span>
            </button>
          </div>
        </BackgroundGradient>
      </div>
    </AuroraBackground>
  );
}
