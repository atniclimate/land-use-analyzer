import { StoryViewScaffold } from "@/components/story/StoryViewScaffold";
import { getStoryView } from "@/lib/site";

export function FloodView() {
  return <StoryViewScaffold view={getStoryView("flood")} />;
}
