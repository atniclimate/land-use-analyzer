import { StoryViewScaffold } from "@/components/story/StoryViewScaffold";
import { getStoryView } from "@/lib/site";

export function ChangingHandsView() {
  return <StoryViewScaffold view={getStoryView("changing-hands")} />;
}
