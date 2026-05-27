import { StoryViewScaffold } from "@/components/story/StoryViewScaffold";
import { getStoryView } from "@/lib/site";

export function DroughtView() {
  return <StoryViewScaffold view={getStoryView("drought")} />;
}
