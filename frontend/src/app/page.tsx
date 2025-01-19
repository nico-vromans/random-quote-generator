"use client";

import React, { useEffect, useState } from "react";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { ModeToggle } from "@/components/ui/mode-toggle";
import { BackgroundGradient } from "@/components/ui/background-gradient";
import { Badge } from "@/components/ui/badge"
import { FaRegThumbsDown, FaRegThumbsUp, FaThumbsDown, FaThumbsUp } from "react-icons/fa6";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger, } from "@/components/ui/popover"

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
      fetch(data.image_url, { method: 'HEAD' }).catch(() => null)
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
      fetch(data.image_url, { method: 'HEAD' }).catch(() => null)
    );

    data.is_image_accessible = imageResponse?.ok || false;
    setQuoteData(data); // Save the data to state
  }

  // Fetch a random quote from the Quote API
  const fetchRandomQuote = async () => {
    setLoading(true);
    try {
      const response = await fetch(baseQuotesUrl + "get_random_quote/", { method: "GET" });
      const data = await response.json();
      const imageResponse = await Promise.resolve(
        fetch(data.image_url, { method: 'HEAD' }).catch(() => null)
      );

      data.is_image_accessible = imageResponse?.ok || false;
      setQuoteData(data); // Save the data to state
    } catch (error) {
      console.error("Error fetching quote data:", error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch a random quote with a specific category from the Quote API
  const fetchQuoteByCategory = async (category: string) => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({ category: category })
      const response: Response = await fetch(baseQuotesUrl + "get_random_quote_by_category/?" + queryParams.toString(), { method: "GET" });
      const data = await response.json();
      const imageResponse: Response | null = await Promise.resolve(
        fetch(data.image_url, { method: 'HEAD' }).catch(() => null)
      );

      data.is_image_accessible = imageResponse?.ok || false;
      setQuoteData(data); // Save the data to state
    } catch (error) {
      console.error("Error fetching quote data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRandomQuote();

    const handleKeyDown = (event: any) => {
      if (event.key.toLowerCase() === ' ') {
        fetchRandomQuote(); // Fetch new quote on key press
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const {
    guid,
    author,
    quote_text,
    category,
    likes,
    dislikes,
    image_url,
    is_image_accessible
  } = quoteData || {
    'guid': '',
    'author': 'Some Author',
    'quote_text': 'Some very inspiring default quote text.',
    'category': 'category',
    'likes': 0,
    'dislikes': 0,
    'image_url': 'https://images.unsplash.com/photo-1503797172624-decbe212fdb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2OTU3MTR8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MzczMTIwODh8&ixlib=rb-4.0.3&q=80&w=1080',
    'is_image_accessible': true,
  };

  return (
    <AuroraBackground>
      <div className="absolute top-10 right-10 z-50">
        <ModeToggle />
      </div>
      <div className="absolute top-20 right-10 z-50">
        <Popover defaultOpen={true}>
          <PopoverTrigger asChild className="w-9 h-9">
            <Button variant="outline" className="text-accent-foreground">?</Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto mr-10">
            <div className="grid gap-4">
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">Press spacebar to get a new random quote.</p>
                <p className="text-sm text-muted-foreground">
                  Click the category to get a new random quote from the same category.
                </p>
              </div>
            </div>
          </PopoverContent>
        </Popover>
      </div>
      <div>
        <BackgroundGradient className={cn(
          "rounded-lg p-3 sm:p-10 bg-white dark:bg-zinc-900",
          { "blur-sm pointer-events-none": loading }
        )}>
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
                &quot;{quote_text ? quote_text : ''}&quot;
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
                      "flex flex-col items-center px-6 py-2 bg-transparent border-2 dark:text-white " +
                      "text-black rounded-lg font-bold transform hover:-translate-y-1 transition duration-400",
                      { "border-green-700 dark:border-green-700": getPreviousVote(guid) === 'like' },
                      { "border-black dark:border-white": getPreviousVote(guid) !== 'like' },
                    )}>
              {getPreviousVote(guid) === 'like' ? <FaThumbsUp className="text-green-700" /> : <FaRegThumbsUp />}
              <span>{likes}</span>
            </button>
            <div className="align-middle content-center">
              <Badge className="cursor-pointer"
                     onClick={() => fetchQuoteByCategory(category['name'])}>{category['name']}</Badge>
            </div>
            <button onClick={dislikeQuote}
                    className={cn(
                      "flex flex-col items-center px-6 py-2 bg-transparent border-2 dark:text-white " +
                      "text-black rounded-lg font-bold transform hover:-translate-y-1 transition duration-400",
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
